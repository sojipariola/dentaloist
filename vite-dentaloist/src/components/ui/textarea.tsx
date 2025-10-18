import React from 'react'
import { clsx } from 'clsx'

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  variant?: 'default' | 'error'
  resize?: 'none' | 'vertical' | 'horizontal' | 'both'
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, variant = 'default', resize = 'vertical', ...props }, ref) => {
    const variantStyles = {
      default: 'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
      error: 'border-red-500 focus:border-red-500 focus:ring-red-500',
    }

    const resizeStyles = {
      none: 'resize-none',
      vertical: 'resize-y',
      horizontal: 'resize-x',
      both: 'resize',
    }

    return (
      <textarea
        className={clsx(
          'flex w-full rounded-lg border bg-white px-3 py-2 text-sm placeholder:text-gray-400',
          'focus:outline-none focus:ring-2 focus:ring-offset-1',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'transition-colors duration-200',
          variantStyles[variant],
          resizeStyles[resize],
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)

Textarea.displayName = 'Textarea'

export { Textarea }