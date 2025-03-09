import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const BookDetail = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/books/${id}/`);
        setBook(response.data);
      } catch (error) {
        console.error('Error fetching book:', error);
      }
    };

    fetchBook();
  }, [id]);

  if (!book) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="max-w-4xl mx-auto">
        <img
          src={book.thumbnailUrl}
          alt={book.title}
          className="w-full h-64 object-cover rounded-lg mb-4"
        />
        <h1 className="text-3xl font-bold mb-4">{book.title}</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-gray-600">{book.shortDescription}</p>
            <div className="mt-4">
              <p><strong>Language:</strong> {book.language}</p>
              <p><strong>Year:</strong> {book.year}</p>
              <p><strong>Has Audio:</strong> {book.hasAudio ? 'Yes' : 'No'}</p>
              <p><strong>Has File:</strong> {book.hasFile ? 'Yes' : 'No'}</p>
            </div>
          </div>
          {book.hasFile && (
            <div className="border rounded-lg p-4">
              <h2 className="text-xl font-semibold mb-2">Download</h2>
              <a
                href={book.filePath}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                target="_blank"
                rel="noopener noreferrer"
              >
                Download File
              </a>
            </div>
          )}
        </div>
        <div className="mt-4">
          <h2 className="text-2xl font-semibold mb-2">Content</h2>
          <div dangerouslySetInnerHTML={{ __html: book.html }} />
        </div>
      </div>
    </div>
  );
};

export default BookDetail; 