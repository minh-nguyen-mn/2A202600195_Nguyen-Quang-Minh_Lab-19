# LAB DAY 19 — XÂY DỰNG HỆ THỐNG GRAPHRAG

## 1. Mục tiêu

- Hiểu quy trình trích xuất thực thể (Entity Extraction) và quan hệ (Relation Extraction)
- Xây dựng pipeline GraphRAG hoàn chỉnh
- So sánh GraphRAG với Flat RAG
- Phân tích độ chính xác và hiện tượng hallucination

---

## 2. Tổng quan hệ thống

### 2.1 Pipeline

Hệ thống được xây dựng theo các bước:

1. **Entity & Relation Extraction**
   - Sử dụng LLM để trích xuất triples từ văn bản

2. **Graph Construction**
   - Xây dựng đồ thị tri thức bằng NetworkX

3. **Query Processing**
   - Trích xuất entity từ câu hỏi
   - Duyệt đồ thị bằng BFS (2-hop)
   - Chuyển graph → text

4. **Answer Generation**
   - LLM trả lời dựa trên context từ graph

---

## 3. Giải thích các khái niệm

### 3.1 Entity Extraction

LLM được sử dụng để phân biệt:

- **Entity (Node):**
  - Ví dụ: OpenAI, Google, Microsoft
- **Relation:**
  - Ví dụ: FOUNDED_BY, FOUNDED_IN

Phương pháp:
- Sử dụng prompt ràng buộc format `(Entity, Relation, Entity)`
- Parse thành danh sách triples

---

### 3.2 Graph Construction & Deduplication

Vấn đề:
- "OpenAI" và "openai" có thể trở thành 2 node khác nhau

Giải pháp:
- Chuẩn hóa dữ liệu (lowercase)
- Chuẩn hóa relation (uppercase, underscore)

Ý nghĩa:
- Tránh trùng lặp node
- Đảm bảo BFS traversal chính xác

---

### 3.3 BFS vs Vector Search

| Phương pháp | Đặc điểm |
|------------|--------|
| BFS (GraphRAG) | Duyệt theo quan hệ trong graph |
| Vector Search (Flat RAG) | Tìm theo độ tương đồng ngữ nghĩa |

Khác biệt:
- GraphRAG → reasoning theo cấu trúc
- Flat RAG → matching theo ngữ nghĩa

---

## 4. Kết quả thực nghiệm

### 4.1 Đặc điểm dữ liệu

Corpus gồm 3 câu:

- OpenAI – founder, year  
- Google – founder, year  
- Microsoft – founder, year  

Đây là dataset đơn giản, không yêu cầu reasoning phức tạp.

---

### 4.2 Nhận xét tổng quan

- Cả Flat RAG và GraphRAG đều đạt độ chính xác cao
- Không có sự khác biệt lớn về correctness
- Khác biệt chủ yếu nằm ở cách biểu diễn kết quả

---

### 4.3 So sánh chi tiết

#### 1. Độ chính xác

Ví dụ:

**Who founded OpenAI?**

- Flat RAG → đúng  
- GraphRAG → đúng  

👉 Cả hai đều hoạt động tốt với dữ liệu đơn giản

---

#### 2. Format output

**Which company was founded in 2015?**

- Flat RAG:
  → "OpenAI was founded in 2015."

- GraphRAG:
  → "openai"

👉 GraphRAG trả về entity (node), Flat RAG trả về câu

---

#### 3. Multi-hop reasoning

**Give founders and year of OpenAI**

- Flat RAG:
  → lấy nguyên câu từ corpus

- GraphRAG:
  → kết hợp nhiều quan hệ:
    - FOUNDED_BY
    - FOUNDED_IN

👉 GraphRAG hỗ trợ multi-hop reasoning

---

#### 4. Hallucination

GraphRAG đôi khi trả lời:

- "December 2015"
- "September 1998"

👉 Đây là thông tin không có trong corpus

Nguyên nhân:
- LLM bổ sung kiến thức ngoài context

👉 Flat RAG ít bị hiện tượng này hơn

---

### 4.4 Bảng so sánh

| Tiêu chí | Flat RAG | GraphRAG |
|--------|----------|----------|
| Accuracy | Cao | Cao |
| Output tự nhiên | Cao | Trung bình |
| Output dạng entity | Thấp | Cao |
| Multi-hop reasoning | Không rõ | Có |
| Hallucination | Thấp | Cao hơn |

---

## 5. Phân tích

### 5.1 Khi nào GraphRAG hiệu quả?

- Dữ liệu lớn
- Nhiều quan hệ
- Cần multi-hop reasoning

Ví dụ:
- "Ai là co-founder của công ty được thành lập năm 2015?"

---

### 5.2 Khi nào Flat RAG đủ tốt?

- Dữ liệu nhỏ
- Thông tin trực tiếp trong văn bản
- Không cần suy luận nhiều bước

👉 Trường hợp của bài lab này

---

### 5.3 Insight quan trọng

GraphRAG không cải thiện đáng kể accuracy trong dataset nhỏ, nhưng:

- Cung cấp cấu trúc tri thức rõ ràng
- Dễ mở rộng cho hệ thống lớn

---

## 6. Chi phí (Cost Analysis)

### 6.1 Token usage

- Extraction: ~200–400 tokens
- Query: ~100 tokens/câu

→ Tổng chi phí thấp

---

### 6.2 Thời gian

| Bước | Thời gian |
|------|----------|
| Embedding | Nhanh |
| Extraction | Chậm nhất |
| Query | Trung bình |

---

### 6.3 Nhận xét

- GraphRAG tốn chi phí ban đầu (build graph)
- Nhưng giúp tăng khả năng reasoning

---

## 7. Kết luận

- Cả Flat RAG và GraphRAG đều hiệu quả với dữ liệu nhỏ
- GraphRAG không vượt trội về accuracy trong bài này
- Tuy nhiên:
  - tổ chức tri thức tốt hơn
  - hỗ trợ reasoning tốt hơn

👉 GraphRAG phù hợp cho hệ thống lớn và phức tạp

---

## 8. Deliverables

- Source code: thư mục `src/`
- Kết quả đánh giá: `outputs/evaluation.csv`
- Visualization: `outputs/graph.png`