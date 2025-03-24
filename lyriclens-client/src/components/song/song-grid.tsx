import React from "react";
import { SongCard } from "./song-card";
import { cn } from "@/lib/utils";

import { ISongGridProps, ISong } from "@/types";
import Skeleton from "@/components/ui/skeleton";

export const SongGrid: React.FC<ISongGridProps> = ({
	songs,
	onSongClick,
	isLoading = false,
	emptyMessage = "No songs found",
	className,
}) => {

	const handleSongClick = (song: ISong) => {
		if (onSongClick) {
			onSongClick(song);
		}
	};

	if (isLoading) {
		return (
			<Skeleton className={className} />
		);
	}

	if (songs.length === 0) {
		return (
			<div className={cn("flex items-center justify-center p-8 text-center text-muted-foreground", className)}>
				<p>{emptyMessage}</p>
			</div>
		);
	}

	return (
		<div className={cn("grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5", className)}>
			{songs.map((song) => (
				<SongCard
					key={song.id}
					{...song}
					onClick={handleSongClick}
				/>
			))}
		</div>
	);
};

export default SongGrid; 