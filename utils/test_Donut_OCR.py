import unittest
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from datasets import load_dataset
import re
from PIL import Image
import json

class TestDonutModel(unittest.TestCase):

    def setUp(self):
        # Initialize the processor and model
        print("setup started")
        self.processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-rvlcdip")
        self.model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-rvlcdip")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.image = Image.open("example_receipt.jpg")
        print("setup complete")

    def test_model_output(self):
        print("start testing")
        # Get a sample image from the dataset
        image = self.image

        # Prepare decoder inputs
        task_prompt = "<s_rvlcdip>"
        decoder_input_ids = self.processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
        pixel_values = self.processor(image, return_tensors="pt").pixel_values

        # Generate output with the model
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
        print(outputs)

        sequence = self.processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(self.processor.tokenizer.pad_token, "")
        cleaned_sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token

        # Save the OCR'd text to a file
        with open('ocr_output.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(cleaned_sequence)
        
        # Validate the sequence
        # Here we assume that the sequence should not be empty and should be a valid JSON
        json_output = self.processor.token2json(sequence)
        self.assertIsInstance(json_output, dict, "The output should be a dictionary.")
        self.assertTrue(json_output, "The output dictionary should not be empty.")\


if __name__ == '__main__':
    unittest.main()