from catalog.models import Book

books = []
for i in range(1,301):
    books.append(Book(
        title=f'Livro Exemplo {i}',
        author=f'Autor Exemplo {i}',
        isbn=f'EX{i:010d}',
        copies_total=(i % 5) + 1,
    ))

Book.objects.bulk_create(books)
print('300 livros criados')
