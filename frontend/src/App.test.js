import { render, screen } from '@testing-library/react';
import App from './App';

test('renders login page on initial load', () => {
  render(<App />);
  const loginInput = screen.getByPlaceholderText(/Login/i);
  expect(loginInput).toBeInTheDocument();
});