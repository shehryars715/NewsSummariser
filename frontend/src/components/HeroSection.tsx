import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { Search, Sparkles, Loader2, Copy, Share2 } from 'lucide-react';
import { searchArticles, queryWithAISummary, Article } from '@/lib/api';
import { ArticleCard } from '@/components/ArticleCard';
import { useToast } from '@/hooks/use-toast';

const quickQueries = [
  "Pakistan cricket team",
  "Technology startups", 
  "Economic policy",
  "Sports highlights",
  "Business news"
];

export function HeroSection() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Article[]>([]);
  const [aiSummary, setAiSummary] = useState<string>('');
  const [aiArticles, setAiArticles] = useState<Article[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const { toast } = useToast();

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    setShowResults(true);
    setAiSummary('');
    setAiArticles([]);
    
    try {
      const results = await searchArticles(searchQuery, 8);
      setSearchResults(results.articles);
      toast({
        title: "Search completed",
        description: `Found ${results.articles.length} articles`,
      });
    } catch (error) {
      toast({
        title: "Search failed",
        description: "Failed to search articles",
        variant: "destructive",
      });
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleAIQuery = async () => {
    if (!searchQuery.trim()) return;
    
    setIsGeneratingSummary(true);
    setShowResults(true);
    setSearchResults([]);
    
    try {
      const startTime = Date.now();
      const result = await queryWithAISummary(searchQuery, 3);
      const endTime = Date.now();
      const duration = ((endTime - startTime) / 1000).toFixed(1);
      
      setAiSummary(result.summary);
      setAiArticles(result.articles_used || []);
      toast({
        title: "AI Summary generated",
        description: `Summary generated in ${duration}s`,
      });
    } catch (error) {
      toast({
        title: "AI Summary failed",
        description: "Failed to generate AI summary",
        variant: "destructive",
      });
      setAiSummary('');
      setAiArticles([]);
    } finally {
      setIsGeneratingSummary(false);
    }
  };

  const handleCopySummary = () => {
    navigator.clipboard.writeText(aiSummary);
    toast({
      title: "Copied to clipboard",
      description: "AI summary copied to clipboard",
    });
  };

  const handleShareSummary = () => {
    if (navigator.share) {
      navigator.share({
        title: 'AI News Summary',
        text: aiSummary,
      });
    } else {
      handleCopySummary();
    }
  };

  const handleQuickQuery = (query: string) => {
    setSearchQuery(query);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <>
      <section className="hero-gradient py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-primary/10" />
        <div className="container mx-auto px-4 text-center relative z-10">
          <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6 tracking-tight">
            AI-Powered News Intelligence
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground mb-12 max-w-3xl mx-auto leading-relaxed">
            Search, analyze, and summarize Pakistani news with advanced AI. 
            Get intelligent insights from trusted sources instantly.
          </p>

          <div className="max-w-3xl mx-auto mb-8">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <Input
                  placeholder="Search for news, topics, or ask AI anything..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="h-14 text-lg border-2 border-border bg-background/50 backdrop-blur-sm shadow-lg"
                />
              </div>
              <div className="flex gap-3">
                <Button 
                  size="lg" 
                  onClick={handleSearch}
                  disabled={!searchQuery.trim() || isSearching}
                  className="h-14 px-8 btn-gradient text-white font-semibold"
                >
                  {isSearching ? (
                    <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                  ) : (
                    <Search className="h-5 w-5 mr-2" />
                  )}
                  Search
                </Button>
                <Button 
                  size="lg" 
                  variant="outline"
                  onClick={handleAIQuery}
                  disabled={!searchQuery.trim() || isGeneratingSummary}
                  className="h-14 px-8 border-2 border-primary/20 bg-background/50 backdrop-blur-sm hover:bg-primary/5"
                >
                  {isGeneratingSummary ? (
                    <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                  ) : (
                    <Sparkles className="h-5 w-5 mr-2" />
                  )}
                  AI Summary
                </Button>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap justify-center gap-3">
            <span className="text-sm text-muted-foreground font-medium">Quick queries:</span>
            {quickQueries.map((query, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-all duration-200 hover:scale-105 px-4 py-2"
                onClick={() => handleQuickQuery(query)}
              >
                {query}
              </Badge>
            ))}
          </div>
        </div>
      </section>

      {showResults && (
        <section className="py-16 bg-muted/30">
          <div className="container mx-auto px-4">
            {aiSummary && (
              <div className="mb-12">
                <Card className="card-gradient p-8 max-w-4xl mx-auto">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-foreground flex items-center gap-2">
                      <Sparkles className="h-6 w-6 text-primary" />
                      AI Summary
                    </h2>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" onClick={handleCopySummary}>
                        <Copy className="h-4 w-4" />
                      </Button>
                      <Button size="sm" variant="outline" onClick={handleShareSummary}>
                        <Share2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <div className="prose prose-lg max-w-none">
                    <p className="text-foreground leading-relaxed whitespace-pre-wrap">{aiSummary}</p>
                  </div>
                  {aiArticles.length > 0 && (
                    <div className="mt-8">
                      <p className="text-sm text-muted-foreground mb-4">
                        Based on {aiArticles.length} articles:
                      </p>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {aiArticles.map((article, index) => (
                          <ArticleCard key={article.id || index} article={article} />
                        ))}
                      </div>
                    </div>
                  )}
                </Card>
              </div>
            )}

            {searchResults.length > 0 && (
              <div>
                <h2 className="text-3xl font-bold text-foreground mb-8 text-center">
                  Search Results ({searchResults.length} articles found)
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {searchResults.map((article, index) => (
                    <ArticleCard key={article.id || index} article={article} />
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      )}
    </>
  );
}