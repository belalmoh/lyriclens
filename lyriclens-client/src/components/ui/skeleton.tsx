import { cn } from "@/lib/utils";

const Skeleton = ({ className }: { className?: string }) => {
    return (
        <div className={cn("grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5", className)}>
            {Array.from({ length: 10 }).map((_, index) => (
                <div key={index} className="space-y-3">
                    <div className="aspect-square animate-pulse rounded-md bg-muted"></div>
                    <div className="space-y-2">
                        <div className="h-4 w-4/5 animate-pulse rounded bg-muted"></div>
                        <div className="h-3 w-3/5 animate-pulse rounded bg-muted"></div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Skeleton;