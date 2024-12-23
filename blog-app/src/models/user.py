class Article(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(nullable=False)

    def __str__(self):
        return "{" + f"id:{self.id}, title:{self.title}, author_id:{self.author_id}" + "}"

    def as_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content, "author_id": self.author_id}