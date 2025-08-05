#  Advanced RAG Pipeline with Contextual Embeddings

---

##  Introduction

This project builds an **advanced RAG (Retrieval-Augmented Generation) pipeline** that implements **contextual embeddings**—a technique that enhances document chunks by adding contextual descriptions to improve retrieval accuracy.

---

## Traditional RAG Limitations

Traditional RAG systems typically use semantic embeddings with text splitters (such as `recursive character text splitters`) to break documents into chunks. While these approaches excel at finding semantically similar content, they often fail to preserve important contextual relationships between chunks.

### Core Problem

```
Document → Chunks → Embeddings → Retrieval
    ↓
 Context Loss: Isolated chunks lose surrounding information
 Poor Relationships: No understanding of chunk dependencies  
 Reduced Accuracy: Missing contextual clues affect relevance
```

---

##  Contextual Embeddings Solution

Using a **Large Language Model (LLM)** to generate contextual descriptions for each chunk.

### Context Integration Process

These descriptions incorporate information from:

```
<document> 
{{WHOLE_DOCUMENT}} 
</document> 
Here is the chunk we want to situate within the whole document 
<chunk> 
{{CHUNK_CONTENT}} 
</chunk> 
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. 
```

### Benefits

```diff
+ Maintains semantic relationships across chunks
+ Provides richer contextual representations  
+ Improves retrieval relevance and accuracy
+ Reduces information fragmentation
```

---

## BM25 Integration

**BM25** is a probabilistic ranking function based on **TF-IDF** _(Term Frequency-Inverse Document Frequency)_ principles.

### Why BM25?

| Search Type         | Strength                 | Weakness                    |
| ------------------- | ------------------------ | --------------------------- |
| **Semantic Search** | Conceptual similarity    | Exact match struggles       |
| **BM25**            | Precise keyword matching | Poor semantic understanding |

### BM25 Excels At:

-  **Names and proper nouns**
-  **Phone numbers and addresses**
-  **Product codes and technical terms**
-  **Exact phrases and terminology**

> **Result**: A hybrid system that handles both conceptual queries and precise factual lookups.

---

##  Reranking Strategy

Since our pipeline employs a **hybrid approach** combining semantic similarity search with exact keyword matching, a sophisticated reranking system is essential.

### Reranker Functions:

```mermaid
graph LR
    A[Semantic Results] --> C[Reranker]
    B[BM25 Results] --> C[Reranker]
    C --> D[Balanced Final Ranking]
```

- **Balances** results from both semantic and keyword-based retrieval
- **Prevents bias** toward either approach
- **Optimizes ranking** based on query type and context
- **Ensures relevance** regardless of retrieval method


##  Pipeline Architecture

```mermaid
graph TB
    %% Preprocessing Part
    subgraph "Part 1: Preprocessing"
        A[Upload Document] --> B[Text Processing]
        B --> B1[OCR?]
        B --> B2[Context Optimized?]
        B1 --> B2
        B2 --> C[Document Chunking]
        
        C --> D1[Chunk 1]
        C --> D2[Chunk 2]
        C --> D3[...]
        C --> DX[Chunk X]
        
        D1 --> E1[Contextual Prompts]
        D2 --> E2[Contextual Prompts]
        D3 --> E3[Contextual Prompts]
        DX --> EX[Contextual Prompts]
        
        E1 --> F1[Context 1 + Chunk 1]
        E2 --> F2[Context 2 + Chunk 2]
        E3 --> F3[...]
        EX --> FX[Context X + Chunk X]
        
        F1 --> G[Embedding Model]
        F2 --> G
        F3 --> G
        FX --> G
        F1 --> Z[TF-IDF]
        F2 --> Z
        F3 --> Z
        FX --> Z
        G --> H1[Vector Database]
        Z --> H2[TF-IDF Index]
    end
    
    %% Processing Part
    subgraph "Part 2: Processing"
        I[Query] --> H1
        I --> H2
        
        H1 --> J[Rank Fusion]
        H2 --> J
        
        J --> K[Reranker]
        K --> L[LLM Generated Content]
    end
```

