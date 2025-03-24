import { ISuggestionItem, ISong, ILyricsAnalysis } from "@/types";
import { useState } from "react";

const useLyricLens = () => {
	const [songs, setSongs] = useState<ISong[]>([]);
	const [lyrics, setLyrics] = useState<string | null>(null);
	const [lyricsAnalysis, setLyricsAnalysis] = useState<ILyricsAnalysis | null>(null);
	const [isLoading, setIsLoading] = useState<boolean>(false);
	const [error, setError] = useState<string | null>(null);

	const searchSongs = async (query: string) => {
		setIsLoading(true);
		setError(null);

		try {
			const response = await fetch(
				`http://localhost:8000/api/song/search?query=${encodeURIComponent(
					query
				)}`
			);

			if (!response.ok) {
				throw new Error(`Error: ${response.statusText}`);
			}

			const data = await response.json();

			if (data.suggestions && Array.isArray(data.suggestions)) {
				setSongs(
					data.suggestions.map((song: ISuggestionItem) => ({
						id: song.title + "-" + song.artist, // Create a unique ID
						title: song.title,
						artist: song.artist,
						coverUrl: song.cover_url,
					}))
				);
			} else {
				setSongs([]);
				if (data.error) {
					setError(data.error);
				}
			}
		} catch (err) {
			setError(
				err instanceof Error
					? err.message
					: "An error occurred while searching for songs"
			);
			setSongs([]);
		} finally {
			setIsLoading(false);
		}
	};

	const getLyrics = async (song: ISong) => {
		setIsLoading(true);
		setError(null);

		try {
			const response = await fetch(
				`http://localhost:8000/api/song/lyrics?artist_name=${encodeURIComponent(song.artist)}&track_name=${encodeURIComponent(song.title)}`
			);

			if (!response.ok) {
				throw new Error(`Error: ${response.statusText}`);
			}

			const data = await response.json();
			setLyrics(data.lyrics);
		} catch (err) {
			setError(err instanceof Error ? err.message : "An error occurred while fetching lyrics");
		} finally {
			setIsLoading(false);
		}
	};

	const analyzeLyrics = async (song: ISong, lyrics: string) => {
		setIsLoading(true);
		setError(null);

		try {
			const response = await fetch(
				`http://localhost:8000/api/song/analyze`,
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ track_name: song.title, artist_name: song.artist, lyrics: lyrics }),
				}
			);

			if (!response.ok) {
				throw new Error(`Error: ${response.statusText}`);
			}

			const data = await response.json();
			setLyricsAnalysis(data);
		} catch (err) {
			setError(err instanceof Error ? err.message : "An error occurred while analyzing lyrics");
		} finally {
			setIsLoading(false);
		}
	};


	return { songs, lyrics, lyricsAnalysis, isLoading, error, searchSongs, getLyrics, analyzeLyrics };
};

export default useLyricLens;
