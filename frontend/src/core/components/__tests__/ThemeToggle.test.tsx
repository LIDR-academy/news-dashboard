import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeToggle } from '../ThemeToggle';

// Mock next-themes
const mockSetTheme = vi.fn();
const mockUseTheme = vi.fn();

vi.mock('next-themes', () => ({
  useTheme: () => mockUseTheme(),
}));

// Mock lucide-react icons
vi.mock('lucide-react', () => ({
  Moon: ({ className, 'aria-hidden': ariaHidden }: any) => (
    <div data-testid="moon-icon" className={className} aria-hidden={ariaHidden}>🌙</div>
  ),
  Sun: ({ className, 'aria-hidden': ariaHidden }: any) => (
    <div data-testid="sun-icon" className={className} aria-hidden={ariaHidden}>☀️</div>
  ),
}));

// Mock Switch component
vi.mock('../../../components/ui/switch', () => ({
  Switch: ({ checked, onCheckedChange, disabled, 'aria-label': ariaLabel, className }: any) => (
    <button
      data-testid="theme-switch"
      onClick={() => !disabled && onCheckedChange && onCheckedChange(!checked)}
      disabled={disabled}
      aria-label={ariaLabel}
      className={className}
      data-checked={checked}
    >
      {checked ? 'ON' : 'OFF'}
    </button>
  ),
}));

describe('ThemeToggle', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render with icons', () => {
    mockUseTheme.mockReturnValue({
      theme: 'light',
      setTheme: mockSetTheme,
      resolvedTheme: 'light',
    });

    render(<ThemeToggle />);

    // Check icons are rendered
    expect(screen.getByTestId('sun-icon')).toBeInTheDocument();
    expect(screen.getByTestId('moon-icon')).toBeInTheDocument();
  });

  it('should render correctly with light theme', async () => {
    mockUseTheme.mockReturnValue({
      theme: 'light',
      setTheme: mockSetTheme,
      resolvedTheme: 'light',
    });

    render(<ThemeToggle />);

    // Wait for component to be mounted
    await waitFor(() => {
      const switchButton = screen.getByTestId('theme-switch');
      expect(switchButton).not.toBeDisabled();
    });

    const switchButton = screen.getByTestId('theme-switch');
    expect(switchButton).toHaveAttribute('data-checked', 'false');
    expect(switchButton).toHaveAttribute('aria-label', 'Switch to dark mode');

    // Check icons are rendered
    expect(screen.getByTestId('sun-icon')).toBeInTheDocument();
    expect(screen.getByTestId('moon-icon')).toBeInTheDocument();

    // Check sun icon has active styling
    const sunIcon = screen.getByTestId('sun-icon');
    expect(sunIcon.className).toContain('text-yellow-500');

    // Check moon icon has inactive styling
    const moonIcon = screen.getByTestId('moon-icon');
    expect(moonIcon.className).toContain('text-gray-400');
  });

  it('should render correctly with dark theme', async () => {
    mockUseTheme.mockReturnValue({
      theme: 'dark',
      setTheme: mockSetTheme,
      resolvedTheme: 'dark',
    });

    render(<ThemeToggle />);

    // Wait for component to be mounted
    await waitFor(() => {
      const switchButton = screen.getByTestId('theme-switch');
      expect(switchButton).not.toBeDisabled();
    });

    const switchButton = screen.getByTestId('theme-switch');
    expect(switchButton).toHaveAttribute('data-checked', 'true');
    expect(switchButton).toHaveAttribute('aria-label', 'Switch to light mode');

    // Check sun icon has inactive styling
    const sunIcon = screen.getByTestId('sun-icon');
    expect(sunIcon.className).toContain('text-gray-400');

    // Check moon icon has active styling
    const moonIcon = screen.getByTestId('moon-icon');
    expect(moonIcon.className).toContain('text-blue-400');
  });

  it('should call setTheme with "dark" when switching from light to dark', async () => {
    mockUseTheme.mockReturnValue({
      theme: 'light',
      setTheme: mockSetTheme,
      resolvedTheme: 'light',
    });

    render(<ThemeToggle />);

    // Wait for component to be mounted
    await waitFor(() => {
      const switchButton = screen.getByTestId('theme-switch');
      expect(switchButton).not.toBeDisabled();
    });

    const switchButton = screen.getByTestId('theme-switch');
    fireEvent.click(switchButton);

    expect(mockSetTheme).toHaveBeenCalledWith('dark');
    expect(mockSetTheme).toHaveBeenCalledTimes(1);
  });

  it('should call setTheme with "light" when switching from dark to light', async () => {
    mockUseTheme.mockReturnValue({
      theme: 'dark',
      setTheme: mockSetTheme,
      resolvedTheme: 'dark',
    });

    render(<ThemeToggle />);

    // Wait for component to be mounted
    await waitFor(() => {
      const switchButton = screen.getByTestId('theme-switch');
      expect(switchButton).not.toBeDisabled();
    });

    const switchButton = screen.getByTestId('theme-switch');
    fireEvent.click(switchButton);

    expect(mockSetTheme).toHaveBeenCalledWith('light');
    expect(mockSetTheme).toHaveBeenCalledTimes(1);
  });

  it('should have proper accessibility attributes', async () => {
    mockUseTheme.mockReturnValue({
      theme: 'light',
      setTheme: mockSetTheme,
      resolvedTheme: 'light',
    });

    render(<ThemeToggle />);

    // Wait for component to be mounted
    await waitFor(() => {
      const switchButton = screen.getByTestId('theme-switch');
      expect(switchButton).not.toBeDisabled();
    });

    const switchButton = screen.getByTestId('theme-switch');
    expect(switchButton).toHaveAttribute('aria-label', 'Switch to dark mode');

    // Icons should have aria-hidden
    const sunIcon = screen.getByTestId('sun-icon');
    const moonIcon = screen.getByTestId('moon-icon');
    expect(sunIcon).toHaveAttribute('aria-hidden', 'true');
    expect(moonIcon).toHaveAttribute('aria-hidden', 'true');
  });

  it('should handle system theme correctly', async () => {
    mockUseTheme.mockReturnValue({
      theme: 'system',
      setTheme: mockSetTheme,
      resolvedTheme: 'light', // System preference is light
    });

    render(<ThemeToggle />);

    // Wait for component to be mounted
    await waitFor(() => {
      const switchButton = screen.getByTestId('theme-switch');
      expect(switchButton).not.toBeDisabled();
    });

    // Should use resolvedTheme, not theme
    const switchButton = screen.getByTestId('theme-switch');
    expect(switchButton).toHaveAttribute('data-checked', 'false');
  });

  it('should handle dark system theme correctly', async () => {
    mockUseTheme.mockReturnValue({
      theme: 'system',
      setTheme: mockSetTheme,
      resolvedTheme: 'dark', // System preference is dark
    });

    render(<ThemeToggle />);

    // Wait for component to be mounted
    await waitFor(() => {
      const switchButton = screen.getByTestId('theme-switch');
      expect(switchButton).not.toBeDisabled();
    });

    // Should use resolvedTheme, not theme
    const switchButton = screen.getByTestId('theme-switch');
    expect(switchButton).toHaveAttribute('data-checked', 'true');
  });
});

