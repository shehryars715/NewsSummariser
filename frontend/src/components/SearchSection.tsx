import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Search, Loader2, SortAsc, SortDesc } from 'lucide-react';
import { ArticleCard } from './ArticleCard';
import { Article, searchArticles } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface SearchSectionProps {
  initialQuery?: string;
}

type SortOption = 'relevance' | 'date' | 'category';
type SortOrder = 'asc' | 'desc';

export function SearchSection({ initialQuery = '' }: SearchSectionProps) {
  const [query, setQuery] = useState(initialQuery);
  const [maxArticles, setMaxArticles] = useState([5]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sortBy, setSortBy] = useState<SortOption>('relevance');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');
  const { toast } = useToast();

  const handleSearch = async () => {
    if (!query.trim()) {
      toast({
        title: "Error",
        description: "Please enter a search query",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      const result = await searchArticles(query, maxArticles[0]);
      let sortedArticles = [...result.articles];

      // Apply sorting
      sortedArticles.sort((a, b) => {
        let comparison = 0;
        
        switch (sortBy) {
          case 'relevance':
            comparison = (b.relevance_score || 0) - (a.relevance_score || 0);
            break;
          case 'date':
            const dateA = new Date(a.publish_time || 0).getTime();
            const dateB = new Date(b.publish_time || 0).getTime();
            comparison = dateB - dateA;
            break;
          case 'category':
            comparison = (a.category || '').localeCompare(b.category || '');
            break;
        }

        return sortOrder === 'asc' ? -comparison : comparison;
      });

      setArticles(sortedArticles);
      
      toast({
        title: "Search Complete",
        description: `Found ${sortedArticles.length} articles`,
      });
    } catch (error) {
      toast({
        title: "Search Failed",
        description: error instanceof Error ? error.message : "Unknown error occurred",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <section className="py-8">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Smart Search
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Search Input */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Input
              placeholder="Enter your search query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button onClick={handleSearch} disabled={isLoading}>
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <Search className="h-4 w-4 mr-2" />
              )}
              Search
            </Button>
          </div>

          {/* Controls */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Article Count Slider */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Max Articles: {maxArticles[0]}</label>
              <Slider
                value={maxArticles}
                onValueChange={setMaxArticles}
                max={10}
                min={1}
                step={1}
                className="w-full"
              />
            </div>

            {/* Sort By */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Sort By</label>
              <Select value={sortBy} onValueChange={(value: SortOption) => setSortBy(value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="relevance">Relevance</SelectItem>
                  <SelectItem value="date">Date</SelectItem>
                  <SelectItem value="category">Category</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Sort Order */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Order</label>
              <Button
                variant="outline"
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="w-full justify-start"
              >
                {sortOrder === 'desc' ? (
                  <SortDesc className="h-4 w-4 mr-2" />
                ) : (
                  <SortAsc className="h-4 w-4 mr-2" />
                )}
                {sortOrder === 'desc' ? 'Descending' : 'Ascending'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results */}
      {articles.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-6">
            Search Results ({articles.length} articles)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article, index) => (
              <ArticleCard 
                key={article.id || index} 
                article={article} 
                showRelevanceScore={true}
              />
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && articles.length === 0 && query && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">No articles found. Try a different search term.</p>
        </div>
      )}
    </section>
  );
}