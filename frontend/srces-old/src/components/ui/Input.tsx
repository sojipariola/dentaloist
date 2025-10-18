interface InputProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  type?: string;
}

export default function Input({ value, onChange, placeholder, type = "text" }: InputProps) {
  return (
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="border p-2 rounded w-full"
    />
  );
}
