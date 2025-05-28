// frontend/src/tests/LoginPage.test.js

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom'; // LoginPage usa useNavigate
import LoginPage from '../pages/LoginPage'; // Ajuste o caminho se a estrutura for diferente

// Mock para useNavigate, já que o componente o utiliza
const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'), // Importa o original
  useNavigate: () => mockedNavigate,         // Sobrescreve useNavigate
}));

// Mock para axios, já que LoginPage faz uma chamada POST para /api/login/
jest.mock('axios');

describe('LoginPage Component', () => {
  beforeEach(() => {
    // Limpa os mocks antes de cada teste
    mockedNavigate.mockClear();
    // Se axios for usado e você quiser resetar chamadas:
    // axios.post.mockClear();
  });

  test('renders login form elements', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    expect(screen.getByPlaceholderText('Login')).toBeInTheDocument(); // Placeholder do seu input de email
    expect(screen.getByPlaceholderText('Senha')).toBeInTheDocument(); // Placeholder do seu input de senha
    expect(screen.getByRole('button', { name: /Entrar/i })).toBeInTheDocument(); // Botão "Entrar"
  });

  test('allows user to type into email and password fields', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('Login');
    const passwordInput = screen.getByPlaceholderText('Senha');

    fireEvent.change(emailInput, { target: { value: 'teste@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'senha123' } });

    expect(emailInput.value).toBe('teste@example.com');
    expect(passwordInput.value).toBe('senha123');
  });

  // Você adicionaria mais testes aqui, por exemplo:
  // - test('calls login API and navigates on successful login')
  // - test('shows error message on failed login')
});