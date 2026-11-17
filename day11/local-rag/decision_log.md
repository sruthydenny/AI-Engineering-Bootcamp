## Machine

- **hardware**: My laptop has an 11th Gen Intel Core i7-11800H processor running at 2.30 GHz, 16 GB DDR4 RAM, Intel UHD Graphics and an NVIDIA GeForce RTX 3050 Laptop GPU. I ran Ollama natively on windows not through WSL
- **`ollama ps` with my main model loaded:**  
      - Name: qwen3.5:4b-q4_K_M
      - Size: 3.9 GB
      - Processor: 52% CPU/ 48% GPU
      - Context: 8192
      - Runner: llamacpp
      - output: 
      PS D:\Sruthy> ollama ps
     NAME                 ID              SIZE      PROCESSOR          CONTEXT    RUNNER      UNTIL              
     qwen3.5:4b-q4_K_M    d8b0f5e9760c    3.9 GB    52%/48%CPU/GPU    8192       llamacpp    4 minutes from now  

## Model Selection

- **Chosen LLM:**  qwen3.5:4b-q4_K_M
- **Thinking:** Off , because I wanted the model to answer without extra reasoning.
- **Why:** I tested the 2 models: 4B and 2B. I compared both models answer quality and the time both models took to respond using benchmark_results.json and here the 4B model got an average rating of 4.14 out of 5 and 2B model got 3.14/5. Comparing both, 2B model was faster but i noticed 4B model gave better answers so i decided to stick with 4B model for my project.
- Additional Experiment :qwen3.5:9b-q4_K_M, I tested addittionaly with 9b using the same benchmark tasks and it scored 5/5 quality but it took more time per answer than 4b model. So i decided to stick with 4b for my final project.
- **What I considered but rejected:** I tested the qwen3.5:2b-q4_K_M, it was faster but it had mistakes in some of the answers it gave and were not as good as 4B model.

## Embedding Model

- **Chosen:** all-minilm (384 dimensions)
- **Why:**  I first used nomic-embed-text first and later i also tested all-minilm which has 384 dimensions to compare the retreival results using the same PDF documents and test questions. Here both model retrieved useful information but their results were different for some questions. all-minilm gave better results for Q08 and Q10 but Q12 was incomplete and some questions such as Q09 was incorrect and The results were close, so I cannot say that one model was clearly better overall. I chose all-minilm for my final configuration.

## Parsing

- **Extractor:** I used PyPDF to extract text from the PDF files with the layout extraction mode and i processed it page by page and kept the information of page in the metadata and for the table extraction i checked the data-classification in security_policy.pdf in page 3 and most of the texts were extracted but some rows and values are split into different lines and the spacing was not perfect even though the table was readable.

## Chunking Strategy

- **Chunk size:** I tested 800 and 500 characters
- **Overlap:** 100 characters
- **Why:** I tested both chunk sizes using all-minilm and Top-K 8. Both 800 and 500 character chunk gave 13 correct answers out of 18 in earlier evaluation and after reviewing Q08 and marking it as failed the 500 character result became 12 out of 18.

## Retrieval Configuration

- **Top-K:** 8 (12/18) questions passed (66.7%) after reviewing 
- **Top-K 4:** 9/18 questions passed (50%).
- **Context window:** 8192
- **Prompt tokens:** 1143 to 1605 tokens (average around 1343 tokens)
- **Why:** I tested Top-K values of 4 and 8 using the same 500 character chunk size and all-minilm embedding model. Top-K 4 gave 9 correct answers out of 18 while Top-K 8 gave 12 correct answers out of 18. So I decided to use Top-K 8 because it gave better results in my tests.

## Observations

- **What worked well:** The system answered 12 out of 18 questions correctly. For example, Q10 gave the correct sick-leave information, and Q16 gave the correct phishing incident level and response times.
- **What failed:** The system got 6 questions wrong. Q01 missed that public holidays are separate from paid leave. Q03 missed the countries for Lisbon and Austin. Q07 missed part of the remote-work policy. Q08 gave the revenue amounts and growth rates but missed the revenue shares. Q09 gave wrong security information. Q12 gave the wrong NRR comparison.
- **Traps I hit:** I noticed that changing the chunk size and Top-K value changed the results. Sometimes the system found useful information but still gave an incomplete or wrong answer. I had to test different settings and check the answers carefully.
- **Local vs cloud expectations:** I think a cloud model might give better answers, but I did not test one. I liked that my local system runs on my own computer and does not need a cloud service.

## If I Had More Time / Better Hardware

- If I had more time, I would try different chunk sizes and embedding models to see if I could get better results. I would also try to improve the answers for the questions the system got wrong. With better hardware, I would test larger local models to see if they could give more accurate answers.
