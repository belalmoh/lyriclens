import React, { useState } from "react";
import { Search } from "lucide-react";
import { cn } from "@/lib/utils";

interface SearchInputProps {
	placeholder?: string;
	onSearch: (query: string) => void;
	className?: string;
}

export const SearchInput: React.FC<SearchInputProps> = ({
	placeholder = "Search...",
	onSearch,
	className,
}) => {
	const [query, setQuery] = useState<string>("");

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		onSearch(query);
	};

	return (
		<form onSubmit={handleSubmit} className={cn("w-full", className)}>
			<div className="relative flex items-center">
				<input
					type="text"
					value={query}
					onChange={(e) => setQuery(e.target.value)}
					placeholder={placeholder}
					className={cn(
						"border-input bg-background text-foreground ring-offset-background",
						"w-full rounded-md border px-4 py-2 pr-10",
						"focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
						"placeholder:text-muted-foreground"
					)}
				/>
				<button
					type="submit"
					className={cn(
						"absolute right-2 rounded-sm p-1",
						"hover:bg-accent hover:text-accent-foreground",
						"focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
					)}
					aria-label="Search"
				>
					<Search className="h-5 w-5" />
				</button>
			</div>
		</form>
	);
};

export default SearchInput; 