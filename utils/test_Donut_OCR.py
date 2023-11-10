
import unittest
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from unittest.mock import patch
from unittest import skip, skipIf

class TestDonutModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the processor and model once for all tests
        print("Class setup started")
        cls.processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-rvlcdip")
        cls.model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-rvlcdip")
        cls.device = "cuda" if torch.cuda.is_available() else "cpu"
        cls.model.to(cls.device)
        print("Class setup complete")

    def setUp(self):
        # Setup that runs before each test method
        self.image = Image.open("example_receipt.jpg")

    @skipIf(not torch.cuda.is_available(), "Skip if no GPU is available")
    def test_model_output_gpu(self):
        # This test will be skipped if no GPU is available
        self._test_model_output()

    @skip("Temporarily skipped")
    def test_model_output_temporarily_skipped(self):
        # This test will always be skipped
        pass

    def _test_model_output(self):
        # The main logic of testing model output, called by other test methods
        print("start testing")
        image = self.image

        task_prompt = "<s_rvlcdip>"
        decoder_input_ids = self.processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
        pixel_values = self.processor(image, return_tensors="pt").pixel_values

        outputs = self.model.generate(
            pixel_values.to(self.device),
            decoder_input_ids=decoder_input_ids.to(self.device),
            max_length=self.model.decoder.config.max_position_embeddings,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )

        sequence = self.processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(self.processor.tokenizer.pad_token, "")
        cleaned_sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()

        with patch('builtins.open') as mock_open:
            mock_open.return_value = mock_open
            mock_open.__enter__.return_value.write.return_value = None
            
            with open('ocr_output.txt', 'w', encoding='utf-8') as text_file:
                text_file.write(cleaned_sequence)

            mock_open.assert_called_once_with('ocr_output.txt', 'w', encoding='utf-8')
            mock_open.__enter__.return_value.write.assert_called_once_with(cleaned_sequence)

        json_output = self.processor.token2json(sequence)
        self.assertIsInstance(json_output, dict, "The output should be a dictionary.")
        self.assertTrue(json_output, "The output dictionary should not be empty.")

if __name__ == '__main__':
    unittest.main()
