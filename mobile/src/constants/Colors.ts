export const Colors = {
  // Modern primary palette - Deep blue with vibrancy
  primary: '#4F46E5', // Modern indigo
  primaryDark: '#4338CA',
  primaryLight: '#6366F1',
  
  // Accent colors
  secondary: '#10B981', // Emerald green
  secondaryDark: '#059669',
  secondaryLight: '#34D399',
  
  // Background and surface
  background: '#F9FAFB', // Subtle off-white
  backgroundAlt: '#F3F4F6', // Alternative background
  surface: '#FFFFFF',
  surfaceElevated: '#FFFFFF',
  
  // Semantic colors
  error: '#EF4444', // Modern red
  success: '#10B981', // Emerald
  warning: '#F59E0B', // Amber
  info: '#3B82F6', // Blue
  
  // Text colors
  onPrimary: '#FFFFFF',
  onSecondary: '#FFFFFF',
  onBackground: '#111827', // Dark gray
  onSurface: '#111827',
  onError: '#FFFFFF',
  
  // Neutral colors
  textPrimary: '#111827',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',
  disabled: '#D1D5DB',
  placeholder: '#9CA3AF',
  border: '#E5E7EB',
  divider: '#F3F4F6',
  backdrop: 'rgba(0, 0, 0, 0.5)',
  
  // Status colors
  statusPending: '#F59E0B',
  statusRunning: '#3B82F6',
  statusCompleted: '#10B981',
  statusFailed: '#EF4444',
  
  // Chart colors - vibrant modern palette
  chartColors: [
    '#4F46E5', // Indigo
    '#10B981', // Emerald
    '#F59E0B', // Amber
    '#EF4444', // Red
    '#8B5CF6', // Violet
    '#3B82F6', // Blue
    '#EC4899', // Pink
    '#14B8A6', // Teal
  ],
  
  // Gradient colors
  gradientStart: '#4F46E5',
  gradientEnd: '#7C3AED',
};

/**
 * Add opacity to a hex color
 * @param color - Hex color string (e.g., '#4F46E5')
 * @param opacity - Opacity value as percentage string (e.g., '08', '15', '20')
 * @returns Color with opacity (e.g., '#4F46E508')
 */
export const withOpacity = (color: string, opacity: string): string => {
  return `${color}${opacity}`;
};

export const Theme = {
  colors: Colors,
  roundness: 12, // Increased for modern look
  spacing: {
    xxs: 2,
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 40,
  },
  fontSize: {
    xs: 11,
    sm: 13,
    md: 15,
    base: 16,
    lg: 18,
    xl: 20,
    xxl: 24,
    xxxl: 32,
    display: 40,
  },
  fontWeight: {
    normal: '400' as '400',
    medium: '500' as '500',
    semibold: '600' as '600',
    bold: '700' as '700',
    extrabold: '800' as '800',
  },
  shadows: {
    small: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.05,
      shadowRadius: 2,
      elevation: 1,
    },
    medium: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    },
    large: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.15,
      shadowRadius: 8,
      elevation: 5,
    },
  },
};
