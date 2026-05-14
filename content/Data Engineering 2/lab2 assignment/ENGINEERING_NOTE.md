# DE2 Lab 2: Text Processing - Inverted Index with GitHub Archive

## Objective
Build an inverted index from real GitHub Archive events to enable fast text search capabilities. Compare Parquet vs CSV storage formats for query latency and disk footprint.

## Architecture
**Data Source**: GitHub Archive (sample_archive_github.json)
- Real public GitHub events transformed into text documents
- Each event becomes a document: event_type + repo_name + actor_login

**Pipeline**:
1. **Ingestion**: Load GitHub events with nested schema (repo, actor)
2. **Transformation**: Extract text content from events
3. **Normalization**: Lowercase, tokenization, stop-words removal
4. **Index Building**: Group by token, collect document IDs, count frequency
5. **Persistence**: Write to Parquet (columnar) and CSV (text)
6. **Query Testing**: Measure latency for term lookups

## Data: GitHub Archive (real public events)
- Documents: GitHub events (PushEvent, IssuesEvent, etc.)
- Content: event type + repository name + actor login
- Tokens: Individual words after normalization
- Index: token → [doc_ids], frequency

## Outputs
- `outputs/lab2/inverted_index/` - Parquet format (compressed, columnar)
- `outputs/lab2/inverted_index_csv/` - CSV format (text, universal)
- `proof/plan_index_build.txt` - Execution plan for index construction
- `proof/plan_query.txt` - Execution plan for term lookup
- `lab2_metrics_log.csv` - Query latencies and storage metrics

## Key Metrics
- Unique terms in index
- Query latency (Parquet vs CSV)
- Disk footprint comparison
- Compression ratio