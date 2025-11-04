import React, { useEffect, useState } from 'react';
import { useTheme } from 'next-themes';
import { Moon, Sun } from 'lucide-react';
import { Switch } from '../../components/ui/switch';

/**
 * ThemeToggle Component
 * 
 * A reusable component that provides a toggle switch for switching between
 * light and dark themes. Uses next-themes for theme management and persists
 * the user's preference in localStorage.
 * 
 * Features:
 * - Visual feedback with Sun/Moon icons
 * - Smooth transitions between themes
 * - Accessibility support (keyboard navigation, ARIA labels)
 * - Respects system theme preference by default
 * 
 * @returns {JSX.Element} The theme toggle switch component
 */
export function ThemeToggle(): JSX.Element {
  const [mounted, setMounted] = useState(false);
  const { setTheme, resolvedTheme } = useTheme();

  // useEffect only runs on the client, so we can safely show the UI
  useEffect(() => {
    setMounted(true);
  }, []);

  // Prevent hydration mismatch by not rendering until mounted
  if (!mounted) {
    return (
      <div className="flex items-center gap-2">
        <Sun className="h-4 w-4 text-gray-400" />
        <Switch disabled aria-label="Loading theme toggle" />
        <Moon className="h-4 w-4 text-gray-400" />
      </div>
    );
  }

  const isDark = resolvedTheme === 'dark';

  const handleToggle = (checked: boolean) => {
    setTheme(checked ? 'dark' : 'light');
  };

  return (
    <div className="flex items-center gap-2">
      <Sun 
        className={`h-4 w-4 transition-colors ${
          isDark ? 'text-gray-400' : 'text-yellow-500'
        }`}
        aria-hidden="true"
      />
      <Switch
        checked={isDark}
        onCheckedChange={handleToggle}
        aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
        className="data-[state=checked]:bg-primary"
      />
      <Moon 
        className={`h-4 w-4 transition-colors ${
          isDark ? 'text-blue-400' : 'text-gray-400'
        }`}
        aria-hidden="true"
      />
    </div>
  );
}

