import React from 'react'
import { clsx } from 'clsx'

interface CardProps {
  children: React.ReactNode
  className?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
  variant?: 'default' | 'outline' | 'ghost'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  padding = 'md',
  variant = 'default',
  shadow = 'sm',
  rounded = 'xl',
}) => {
  const paddingStyles = {
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }

  const variantStyles = {
    default: 'bg-white border border-gray-200',
    outline: 'bg-transparent border border-gray-300',
    ghost: 'bg-transparent border-none shadow-none',
  }

  const shadowStyles = {
    none: 'shadow-none',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
  }

  const roundedStyles = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
  }

  return (
    <div
      className={clsx(
        variantStyles[variant],
        paddingStyles[padding],
        shadowStyles[shadow],
        roundedStyles[rounded],
        className
      )}
    >
      {children}
    </div>
  )
}

// Card sub-components for better structure
interface CardHeaderProps {
  children: React.ReactNode
  className?: string
}

export const CardHeader: React.FC<CardHeaderProps> = ({ children, className }) => {
  return (
    <div className={clsx('pb-4', className)}>
      {children}
    </div>
  )
}

interface CardContentProps {
  children: React.ReactNode
  className?: string
}

export const CardContent: React.FC<CardContentProps> = ({ children, className }) => {
  return (
    <div className={clsx('', className)}>
      {children}
    </div>
  )
}

interface CardFooterProps {
  children: React.ReactNode
  className?: string
}

export const CardFooter: React.FC<CardFooterProps> = ({ children, className }) => {
  return (
    <div className={clsx('pt-4 border-t border-gray-100', className)}>
      {children}
    </div>
  )
}

interface CardTitleProps {
  children: React.ReactNode
  className?: string
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6'
}

export const CardTitle: React.FC<CardTitleProps> = ({ 
  children, 
  className,
  as: Component = 'h3'
}) => {
  return (
    <Component className={clsx(
      'text-lg font-semibold leading-6 text-gray-900',
      className
    )}>
      {children}
    </Component>
  )
}

interface CardDescriptionProps {
  children: React.ReactNode
  className?: string
}

export const CardDescription: React.FC<CardDescriptionProps> = ({ children, className }) => {
  return (
    <p className={clsx(
      'text-sm text-gray-600 mt-1',
      className
    )}>
      {children}
    </p>
  )
}