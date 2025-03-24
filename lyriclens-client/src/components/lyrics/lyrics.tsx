import useLyricLens from "@/hooks/useLyricLens";
import { ISong } from "@/types";
import { useEffect, useState } from "react";
import { ArrowLeft, Loader2 } from "lucide-react";

const Lyrics = ({ song, onBack }: { song: ISong; onBack: () => void }) => {
    const { lyrics, lyricsAnalysis, error, getLyrics, analyzeLyrics } = useLyricLens();
    const [isLyricsLoading, setIsLyricsLoading] = useState(false);
    const [isAnalysisLoading, setIsAnalysisLoading] = useState(false);

    useEffect(() => {
        const fetchLyrics = async () => {
            if (song) {
                setIsLyricsLoading(true);
                await getLyrics(song);
                setIsLyricsLoading(false);
            }
        };
        
        fetchLyrics();
    }, [song]);

    useEffect(() => {
        const fetchAnalysis = async () => {
            if (lyrics) {
                setIsAnalysisLoading(true);
                await analyzeLyrics(song, lyrics);
                setIsAnalysisLoading(false);
            }
        };
        
        fetchAnalysis();
    }, [lyrics]);

    return (
        <div className="mb-6">
            <div className="mb-4 flex items-center cursor-pointer" onClick={onBack}>
                <span 
                    className="mr-2 rounded-full p-1 text-primary"
                >
                    <ArrowLeft className="h-5 w-5" />
                </span>
                <h2 className="text-xl font-semibold">
                    {song.title} <span className="text-muted-foreground">by {song.artist}</span>
                </h2>
            </div>

            {error && (
                <div className="rounded-md bg-destructive/10 p-4 text-destructive mb-4">
                    <p>{error}</p>
                </div>
            )}

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                {/* Lyrics Column */}
                <div className="rounded-md border bg-card p-4 shadow-sm">
                    <h3 className="mb-3 border-b pb-2 text-lg font-medium">Lyrics</h3>
                    
                    {isLyricsLoading ? (
                        <div className="flex h-60 items-center justify-center">
                            <Loader2 className="h-6 w-6 animate-spin text-primary" />
                            <span className="ml-2">Loading lyrics...</span>
                        </div>
                    ) : (
                        <div className="max-h-[500px] overflow-y-auto pr-2 whitespace-pre-line">
                            {lyrics || "No lyrics available"}
                        </div>
                    )}
                </div>

                {/* Analysis Column */}
                <div className="rounded-md border bg-card p-4 shadow-sm">
                    <h3 className="mb-3 border-b pb-2 text-lg font-medium">Analysis</h3>
                    
                    {isAnalysisLoading ? (
                        <div className="flex h-60 items-center justify-center">
                            <Loader2 className="h-6 w-6 animate-spin text-primary" />
                            <span className="ml-2">Analyzing lyrics...</span>
                        </div>
                    ) : lyricsAnalysis ? (
                        <div className="max-h-[500px] overflow-y-auto pr-2">
                            <h4 className="mb-2 font-medium">Summary</h4>
                            <p className="mb-4">{lyricsAnalysis.summary}</p>
                            
                            <h4 className="mb-2 font-medium">Countries Mentioned</h4>
                            {lyricsAnalysis.countries_mentioned && lyricsAnalysis.countries_mentioned.length > 0 ? (
                                <ul className="list-inside list-disc">
                                    {lyricsAnalysis.countries_mentioned.map((country: string, index: number) => (
                                        <li key={index}>{country}</li>
                                    ))}
                                </ul>
                            ) : (
                                <p>No countries mentioned in the lyrics</p>
                            )}
                        </div>
                    ) : (
                        <p>No analysis available</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Lyrics;