import React from "react";
import { Music } from "lucide-react";
import { cn } from "@/lib/utils";
import { ISongCardProps } from "@/types";

export const SongCard: React.FC<ISongCardProps> = ({
	title,
	artist,
	id,
	coverUrl,
	onClick,
	className,
}) => {
	const handleClick = () => {
		onClick({
			id: id.toString(),
			title,
			artist,
			coverUrl
		});
	};

	return (
		<div
			className={cn(
				"group relative flex flex-col overflow-hidden rounded-md border bg-card text-card-foreground shadow-sm transition-all",
				"hover:shadow-md hover:bg-accent/10",
				"cursor-pointer",
				className
			)}
			onClick={handleClick}
		>
			<div className="aspect-square overflow-hidden bg-muted">
				{coverUrl ? (
					<img
						src={coverUrl}
						alt={`${title} by ${artist}`}
						className="h-full w-full object-cover transition-transform group-hover:scale-105"
						loading="lazy"
					/>
				) : (
					<div className="flex h-full w-full items-center justify-center bg-muted text-muted-foreground">
						<Music className="h-12 w-12" />
					</div>
				)}
			</div>
			<div className="flex flex-col p-3">
				<h3 className="font-medium line-clamp-3" title={title}>
					{title}
				</h3>
				<p className="text-sm text-muted-foreground line-clamp-1" title={artist}>
					{artist}
				</p>
			</div>
		</div>
	);
};

export default SongCard; 