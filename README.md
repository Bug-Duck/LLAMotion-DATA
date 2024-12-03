# LLAMotion-DATA
The training data of LLAMotion.

# Fine-tuning

## 1. Process data

```bash
python process_data_jsonl.py
```

## 2. Upload to OpenAI server

```bash
python src/upload.py
```

## 3. Fine-tuning

```bash
python src/train.py
```

## 4. Get the training job

```bash
python src/get.py
```

## 5. Keep the record

```bash
python src/search.py
```

## 6. Re-run the getting script

After the training job is completed, you need to re-run the getting script to get the fine-tuned model name.

```bash
python src/get.py
```

The fine-tuned model name will be saved in the `job.json` file.
