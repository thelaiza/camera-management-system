import { render, screen } from '@testing-library/react';
import App from './App'; // Importa o componente App

test('renders learn react link (ou um texto da sua tela inicial)', () => {
  render(<App />);

  const loginPlaceholder = screen.getByPlaceholderText(/Login/i); // O 'i' torna a busca case-insensitive
  expect(loginPlaceholder).toBeInTheDocument();

});