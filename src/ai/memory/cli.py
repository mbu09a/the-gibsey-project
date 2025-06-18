import argparse, json, textwrap
from .embedding_store import EmbeddingStore

store = EmbeddingStore()

parser = argparse.ArgumentParser(description="Gibsey Memory CLI")
sub = parser.add_subparsers(dest="cmd", required=True)

w = sub.add_parser("write", help="Add text to memory")
w.add_argument("--text", required=True)
w.add_argument("--author", required=True)
w.add_argument("--tags", default="")

s = sub.add_parser("search", help="Query memory")
s.add_argument("--query", required=True)
s.add_argument("--k", type=int, default=5)

args = parser.parse_args()

if args.cmd == "write":
    meta = {"author": args.author, "tags": args.tags.split(",")}
    ent = store.add(args.text, meta)
    print("✔ stored", ent.id)
else:
    hits = store.search(args.query, k=args.k)
    for e, sim in hits:
        print(f"{sim:.3f} │ {e.meta['author'][:8]} │ "
              f"{textwrap.shorten(e.text, 80)}")