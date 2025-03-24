import React, { useState } from "react";
import { SearchInput } from "@/components/search/search-input";
import { SongGrid } from "@/components/song/song-grid";
import SearchStatus from "@/components/search/search-status";
import Lyrics from "@/components/lyrics/lyrics";

import useLyricLens from "@/hooks/useLyricLens";
import { ISong } from "@/types";

const SearchPage: React.FC = () => {
	const [query, setQuery] = useState<string>("");
	const [selectedSong, setSelectedSong] = useState<ISong | null>(null);
	const { songs, isLoading, error, searchSongs } = useLyricLens();

	const handleSearch = async (searchQuery: string) => {
		setQuery(searchQuery);
		if (!searchQuery.trim()) {
			return;
		}
		setSelectedSong(null);
		await searchSongs(searchQuery);

	};

	const handleSongClick = (song: ISong) => {
		setSelectedSong(song);
	};

	return (
		<div className="container mx-auto px-4 py-8">
			<div className="mx-auto max-w-4xl">
				<h1 className="mb-8 text-center text-3xl font-bold text-primary">
					LyricLens Song Analysis
				</h1>

				<div className="mb-8">
					<SearchInput
						placeholder="Search for songs or artists..."
						onSearch={handleSearch}
						className="w-full"
					/>
				</div>

				<SearchStatus
					isLoading={isLoading}
					error={error}
				/>

				{query && !isLoading && !error && !selectedSong && (
					<div className="mb-4">
						<h2 className="text-xl font-semibold text-muted-foreground">
							{songs.length > 0
								? `Results for "${query}"`
								: `No results found for "${query}"`}
						</h2>
					</div>
				)}
				{selectedSong && (
					<Lyrics song={selectedSong} onBack={() => setSelectedSong(null)} />
				)}

				{!selectedSong && (
					<SongGrid
						songs={songs}
						onSongClick={handleSongClick}
						isLoading={isLoading}
						emptyMessage="No songs found. Try another search term."
					/>
				)}
			</div>
		</div>
	);
};

export default SearchPage; 