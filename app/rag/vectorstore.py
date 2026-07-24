class VectorStore:
    def __init__(self, path: str, collection: str):
        self.path = path
        self.collection = collection

    def search(self, query: str, k: int = 3) -> list[str]:
        return [
            "Billing issue: Please check your invoice in Account > Billing.",
            "Account issue: Make sure your email is verified before logging in.",
            "Technical issue: Restart the app and clear cache.",
        ][:k]