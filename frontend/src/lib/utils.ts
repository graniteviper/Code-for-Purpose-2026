import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Utility function to merge Tailwind CSS classes efficiently.
 * Combines 'clsx' for conditional classes and 'twMerge' to resolve Tailwind conflicts.
 * 
 * @param inputs - An array of class values, objects, or arrays.
 * @returns A string of merged and deduplicated class names.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
