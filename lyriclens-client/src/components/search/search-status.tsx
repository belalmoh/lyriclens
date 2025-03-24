import React from "react";
import { AlertCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface SearchStatusProps {
	isLoading?: boolean;
	error?: string | null;
	className?: string;
}

export const SearchStatus: React.FC<SearchStatusProps> = ({
	isLoading = false,
	error = null,
	className,
}) => {
	if (!isLoading && !error) {
		return null;
	}

	return (
		<div
			className={cn("flex w-full items-center justify-center p-6", className)}
		>
			{isLoading && (
				<div className="flex items-center text-primary">
					<Loader2 className="mr-2 h-5 w-5 animate-spin" />
					<span>Searching...</span>
				</div>
			)}

			{error && (
				<div className="flex items-center text-destructive">
					<AlertCircle className="mr-2 h-5 w-5" />
					<span>{error}</span>
				</div>
			)}
		</div>
	);
};

export default SearchStatus;
