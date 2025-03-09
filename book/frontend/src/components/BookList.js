import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const BookList = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/books/');
        setBooks(response.data);
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    };

    fetchBooks();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Books</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {books.map((book) => (
          <Link to={`/book/${book.id}`} key={book.id}>
            <div className="border rounded-lg p-4 hover:shadow-lg transition-shadow">
              <img
                src={book.thumbnailUrl}
                alt={book.title}
                className="w-full h-48 object-cover mb-2"
              />
              <h2 className="text-xl font-semibold">{book.title}</h2>
              <p className="text-gray-600">{book.shortDescription}</p>
              <div className="mt-2">
                <span className="text-sm text-gray-500">Language: {book.language}</span>
                <span className="text-sm text-gray-500 ml-4">Year: {book.year}</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default BookList; 