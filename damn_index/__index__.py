import elasticsearch

def main():
    # Connect to localhost:9200 by default:
    es = elasticsearch.Elasticsearch()

    # Connect to cluster at search1:9200, sniff all nodes and round-robin between them
    es = elasticsearch.Elasticsearch(["localhost:9200"], sniff_on_start=True)

    # Index a document:
    es.index(
        index="my_app",
        doc_type="blog_post",
        id=2,
        body={
        "title": "Elasticsearch clients",
        "content": "Interesting content...",
        "date": '2013, 9, 24',
        }
    )

    # Get the document:
    get = es.get(index="my_app", doc_type="blog_post", id=1)
    print(get)
    
    # Search:
    search = es.search(index="my_app", body={"query": {"match": {"title": "elasticsearch"}}})
    print(search)

if __name__ == '__main__':
    main()
