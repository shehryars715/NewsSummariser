import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ExternalLink, Sparkles, Loader2 } from 'lucide-react';
import { Article, summarizeArticleByUrl } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface ArticleCardProps {
  article: Article;
  showRelevanceScore?: boolean;
  showSummarizeButton?: boolean;
}

const getCategoryStyle = (category?: string) => {
  if (!category) return 'bg-news-category-other text-white';
  
  const cat = category.toLowerCase();
  if (cat.includes('sport') || cat.includes('cricket') || cat.includes('football')) {
    return 'bg-news-category-sports text-white';
  }
  if (cat.includes('tech') || cat.includes('technology') || cat.includes('innovation')) {
    return 'bg-news-category-tech text-white';
  }
  if (cat.includes('business') || cat.includes('corporate') || cat.includes('economy')) {
    return 'bg-news-category-business text-white';
  }
  if (cat.includes('national') || cat.includes('pakistan') || cat.includes('politics')) {
    return 'bg-news-category-national text-white';
  }
  return 'bg-news-category-other text-white';
};

export function ArticleCard({ article, showRelevanceScore = false, showSummarizeButton = true }: ArticleCardProps) {
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [summary, setSummary] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSummarize = async () => {
    if (!article.url) {
      toast({
        title: "Error",
        description: "No URL available for this article",
        variant: "destructive",
      });
      return;
    }

    setIsSummarizing(true);
    const startTime = Date.now();

    try {
      const result = await summarizeArticleByUrl(article.url);
      setSummary(result.summary);
      
      const duration = ((Date.now() - startTime) / 1000).toFixed(1);
      toast({
        title: "Summary Generated",
        description: `Summary generated in ${duration}s`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to generate summary",
        variant: "destructive",
      });
    } finally {
      setIsSummarizing(false);
    }
  };

  return (
    <Card className="h-full flex flex-col card-gradient group">
      <CardContent className="p-6 flex-1 flex flex-col">
        <div className="flex items-center gap-2 mb-3">
          <Badge 
            variant="secondary" 
            className={`${getCategoryStyle(article.category)} font-medium`}
          >
            {article.category}
          </Badge>
          {article.relevance_score && (
            <span className="text-xs text-muted-foreground font-medium">
              {Math.round(article.relevance_score * 100)}% match
            </span>
          )}
        </div>
        
        <h3 className="font-bold text-base mb-3 line-clamp-2 text-foreground leading-tight">
          {article.title}
        </h3>
        
        {article.excerpt && (
          <p className="text-sm text-muted-foreground mb-4 flex-1 line-clamp-3 leading-relaxed">
            {article.excerpt}
          </p>
        )}

        {summary && (
          <div className="bg-news-summary-bg border border-news-summary-border rounded-lg p-4 mb-4">
            <h4 className="font-semibold mb-2 text-news-brand">AI Summary</h4>
            <p className="text-sm text-foreground">{summary}</p>
          </div>
        )}
        
        <div className="flex items-center justify-between mt-auto pt-4 border-t border-border/50">
          <Button variant="ghost" size="sm" asChild className="text-primary hover:text-primary/80 font-medium">
            <a 
              href={article.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-sm"
            >
              Read More <ExternalLink className="h-4 w-4 ml-1" />
            </a>
          </Button>
          
          <Button 
            variant="ghost" 
            size="sm"
            onClick={handleSummarize}
            disabled={isSummarizing}
            className="text-sm hover:bg-primary/10"
          >
            {isSummarizing ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Sparkles className="h-4 w-4" />
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}