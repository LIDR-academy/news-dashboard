import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { BackButton } from '../BackButton';

// Mock react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock the core components
jest.mock('../ui/button', () => ({
  Button: ({ children, onClick, variant, size, className, ...props }: any) => (
    <button onClick={onClick} className={`${variant} ${size} ${className}`} {...props}>
      {children}
    </button>
  ),
}));

jest.mock('lucide-react', () => ({
  ArrowLeft: () => <div data-testid="arrow-left-icon" />,
}));

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('BackButton', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders with default props', () => {
    renderWithRouter(<BackButton />);

    expect(screen.getByText('Back')).toBeInTheDocument();
    expect(screen.getByTestId('arrow-left-icon')).toBeInTheDocument();
  });

  it('renders with custom text', () => {
    renderWithRouter(<BackButton>Go Back</BackButton>);

    expect(screen.getByText('Go Back')).toBeInTheDocument();
    expect(screen.queryByText('Back')).not.toBeInTheDocument();
  });

  it('renders without icon when showIcon is false', () => {
    renderWithRouter(<BackButton showIcon={false} />);

    expect(screen.getByText('Back')).toBeInTheDocument();
    expect(screen.queryByTestId('arrow-left-icon')).not.toBeInTheDocument();
  });

  it('navigates back in history when no props provided', () => {
    renderWithRouter(<BackButton />);

    const button = screen.getByText('Back');
    fireEvent.click(button);

    expect(mockNavigate).toHaveBeenCalledWith(-1);
  });

  it('navigates to specific URL when to prop is provided', () => {
    renderWithRouter(<BackButton to="/dashboard" />);

    const button = screen.getByText('Back');
    fireEvent.click(button);

    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });

  it('calls custom onBack function when provided', () => {
    const mockOnBack = jest.fn();
    renderWithRouter(<BackButton onBack={mockOnBack} />);

    const button = screen.getByText('Back');
    fireEvent.click(button);

    expect(mockOnBack).toHaveBeenCalled();
    expect(mockNavigate).not.toHaveBeenCalled();
  });

  it('prioritizes onBack over to prop', () => {
    const mockOnBack = jest.fn();
    renderWithRouter(<BackButton onBack={mockOnBack} to="/dashboard" />);

    const button = screen.getByText('Back');
    fireEvent.click(button);

    expect(mockOnBack).toHaveBeenCalled();
    expect(mockNavigate).not.toHaveBeenCalled();
  });

  it('applies custom variant', () => {
    renderWithRouter(<BackButton variant="destructive" />);

    const button = screen.getByText('Back');
    expect(button).toHaveClass('destructive');
  });

  it('applies custom size', () => {
    renderWithRouter(<BackButton size="lg" />);

    const button = screen.getByText('Back');
    expect(button).toHaveClass('lg');
  });

  it('applies custom className', () => {
    renderWithRouter(<BackButton className="custom-class" />);

    const button = screen.getByText('Back');
    expect(button).toHaveClass('custom-class');
  });

  it('has correct default classes', () => {
    renderWithRouter(<BackButton />);

    const button = screen.getByText('Back');
    expect(button).toHaveClass('outline');
    expect(button).toHaveClass('sm');
    expect(button).toHaveClass('flex items-center gap-2');
  });

  it('renders with all custom props', () => {
    const mockOnBack = jest.fn();
    renderWithRouter(
      <BackButton
        onBack={mockOnBack}
        variant="default"
        size="lg"
        className="custom-class"
        showIcon={false}
      >
        Custom Back
      </BackButton>
    );

    const button = screen.getByText('Custom Back');
    expect(button).toHaveClass('default');
    expect(button).toHaveClass('lg');
    expect(button).toHaveClass('custom-class');
    expect(screen.queryByTestId('arrow-left-icon')).not.toBeInTheDocument();

    fireEvent.click(button);
    expect(mockOnBack).toHaveBeenCalled();
  });
});
