import json
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from telemetry_core import TelemetryCore

class TestTelemetryCore(unittest.TestCase):
    def test_load_config_file_exists(self):
        config_data = {'webhook_url': 'http://example.com/webhook'}
        config_json = json.dumps(config_data)

        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=config_json)):
            telemetry = TelemetryCore("config.json")
            self.assertEqual(telemetry.webhook_url, 'http://example.com/webhook')

    def test_load_config_file_not_exists(self):
        with patch("os.path.exists", return_value=False):
            telemetry = TelemetryCore("non_existent.json")
            self.assertEqual(telemetry.webhook_url, '')

    def test_load_config_error(self):
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", side_effect=Exception("Read error")):
            telemetry = TelemetryCore("config.json")
            self.assertEqual(telemetry.webhook_url, '')

    def test_update_webhook_url_success(self):
        m = mock_open()
        with patch("os.path.exists", return_value=False), \
             patch("builtins.open", m):
            telemetry = TelemetryCore("config.json")
            new_url = "http://new-webhook.com"
            telemetry.update_webhook_url(new_url)

            self.assertEqual(telemetry.webhook_url, new_url)
            m.assert_called_once_with("config.json", 'w')

            handle = m()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            self.assertEqual(json.loads(written_data), {'webhook_url': new_url})

    def test_update_webhook_url_error(self):
        with patch("os.path.exists", return_value=False), \
             patch("builtins.open", side_effect=Exception("Write error")), \
             patch("builtins.print") as mock_print:
            telemetry = TelemetryCore("config.json")
            new_url = "http://error-webhook.com"
            telemetry.update_webhook_url(new_url)

            self.assertEqual(telemetry.webhook_url, new_url)
            mock_print.assert_called_with("[ComfyUI-n8n-Telemetry] Error saving config: Write error")

    def test_send_telemetry_no_url(self):
        with patch("os.path.exists", return_value=False):
            telemetry = TelemetryCore("config.json")
            with patch("threading.Thread") as mock_thread:
                telemetry.send_telemetry({"test": "data"})
                mock_thread.assert_not_called()

    def test_send_telemetry_with_url(self):
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data='{"webhook_url": "http://test.com"}')):
            telemetry = TelemetryCore("config.json")

            with patch("threading.Thread") as mock_thread:
                payload = {"estado": "inicio"}
                telemetry.send_telemetry(payload)

                mock_thread.assert_called_once()
                target_func = mock_thread.call_args[1]['target']
                self.assertEqual(target_func.__name__, '_send')

if __name__ == '__main__':
    unittest.main()
