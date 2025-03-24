interface ISuggestionItem {
    title: string;
    artist: string;
    album?: string;
    preview_url?: string;
    cover_url?: string;
}

interface ISong {
    id: string;
    title: string;
    artist: string;
    coverUrl?: string;
}

interface ISongCardProps {
    id: string | number;
    title: string;
    artist: string;
    coverUrl?: string;
    onClick: (song: ISong) => void;
    className?: string;
}

interface ISongGridProps {
    songs: Array<Omit<ISongCardProps, 'onClick'>>;
    onSongClick?: (song: ISong) => void;
    isLoading?: boolean;
    emptyMessage?: string;
    className?: string;
}

interface ILyricsAnalysis {
    summary: string;
    countries_mentioned: string[];
}

export type { ISuggestionItem, ISong, ISongCardProps, ISongGridProps, ILyricsAnalysis };