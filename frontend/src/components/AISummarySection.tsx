import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Sparkles, Loader2, Copy, Share2, CheckCircle } from 'lucide-react';
import { ArticleCard } from './ArticleCard';
import { Article, queryWithAISummary } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface AISummarySectionProps {
  initialQuery?: string;
}

export function AISummarySection({ initialQuery = '' }: AISummarySectionProps) {
  const [query, setQuery] = useState(initialQuery);
  const [maxArticles, setMaxArticles] = useState([3]);
  const [summary, setSummary] = useState<string>('');
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();

  const handleQuery = async () => {
    if (!query.trim()) {
      toast({
        title: "Error",
        description: "Please enter a query",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    const startTime = Date.now();

    try {
      const result = await queryWithAISummary(query, maxArticles[0]);
      setSummary(result.summary);
      setArticles(result.articles_used);
      
      const duration = ((Date.now() - startTime) / 1000).toFixed(1);
      toast({
        title: "AI Summary Generated",
        description: `Summary generated in ${duration}s`,
      });
    } catch (error) {
      toast({
        title: "Query Failed",
        description: error instanceof Error ? error.message : "Unknown error occurred",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (summary) {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      toast({
        title: "Copied",
        description: "Summary copied to clipboard",
      });
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleShare = async () => {
    if (navigator.share && summary) {
      try {
        await navigator.share({
          title: 'AI News Summary',
          text: `Query: ${query}\n\nSummary: ${summary}`,
        });
      } catch {
        // Fallback to copy
        handleCopy();
      }
    } else {
      handleCopy();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleQuery();
    }
  };

  return (
    <section className="py-8">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            AI Summary Generator
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Query Input */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Input
              placeholder="Ask AI anything about the news..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button onClick={handleQuery} disabled={isLoading}>
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <Sparkles className="h-4 w-4 mr-2" />
              )}
              Generate Summary
            </Button>
          </div>

          {/* Article Count Control */}
          <div className="space-y-2">
            <label className="text-sm font-medium">
              Articles to analyze: {maxArticles[0]}
            </label>
            <Slider
              value={maxArticles}
              onValueChange={setMaxArticles}
              max={10}
              min={1}
              step={1}
              className="w-full max-w-xs"
            />
          </div>
        </CardContent>
      </Card>

      {/* AI Summary Display */}
      {summary && (
        <Card className="mt-8 bg-news-summary-bg border-news-summary-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-news-brand">AI Summary</CardTitle>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={handleCopy}>
                  {copied ? (
                    <CheckCircle className="h-4 w-4 mr-2" />
                  ) : (
                    <Copy className="h-4 w-4 mr-2" />
                  )}
                  {copied ? 'Copied' : 'Copy'}
                </Button>
                <Button variant="outline" size="sm" onClick={handleShare}>
                  <Share2 className="h-4 w-4 mr-2" />
                  Share
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="prose prose-sm max-w-none">
              <p className="text-foreground leading-relaxed whitespace-pre-wrap">
                {summary}
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Source Articles */}
      {articles.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-6">
            Based on {articles.length} articles
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article, index) => (
              <ArticleCard 
                key={article.id || index} 
                article={article}
                showSummarizeButton={false}
              />
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !summary && query && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">
            Enter a query and click "Generate Summary" to get AI insights
          </p>
        </div>
      )}
    </section>
  );
}