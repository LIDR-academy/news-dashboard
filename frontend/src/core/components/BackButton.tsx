import React from 'react';
import { Button } from '../../components/ui/button';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface BackButtonProps {
  /** Custom back action function. If not provided, uses browser history back */
  onBack?: () => void;
  /** Custom back URL. If provided, navigates to this URL instead of going back */
  to?: string;
  /** Button variant */
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  /** Button size */
  size?: 'default' | 'sm' | 'lg' | 'icon';
  /** Additional CSS classes */
  className?: string;
  /** Button text. Defaults to "Back" */
  children?: React.ReactNode;
  /** Whether to show the arrow icon */
  showIcon?: boolean;
}

export const BackButton: React.FC<BackButtonProps> = ({
  onBack,
  to,
  variant = 'outline',
  size = 'sm',
  className = '',
  children = 'Back',
  showIcon = true,
}) => {
  const navigate = useNavigate();

  const handleBack = () => {
    if (onBack) {
      onBack();
    } else if (to) {
      navigate(to);
    } else {
      navigate(-1);
    }
  };

  return (
    <Button
      variant={variant}
      size={size}
      onClick={handleBack}
      className={`flex items-center gap-2 ${className}`}
    >
      {showIcon && <ArrowLeft className="h-4 w-4" />}
      {children}
    </Button>
  );
};
