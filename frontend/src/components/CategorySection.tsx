import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Loader2, ChevronRight } from 'lucide-react';
import { ArticleCard } from './ArticleCard';
import { Article } from '@/lib/api';
import { supabase } from '@/integrations/supabase/client';

interface CategorySectionProps {
  category: string;
  displayName: string;
  onLoadMore: (category: string) => void;
}

export function CategorySection({ category, displayName, onLoadMore }: CategorySectionProps) {
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showMore, setShowMore] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  useEffect(() => {
    loadCategoryArticles();
  }, [category]);

  const loadCategoryArticles = async (limit = 4) => {
    setIsLoading(true);
    try {
      let query = supabase
        .from('news_articles')
        .select('*')
        .order('publish_time', { ascending: false })
        .limit(limit);

      // Add category filter if not 'latest'
      if (category !== 'latest') {
        query = query.ilike('category', `%${category}%`);
      }

      const { data, error } = await query;
      
      if (error) {
        console.error('Error fetching articles:', error);
        return;
      }

      setArticles(data || []);
    } catch (error) {
      console.error('Error loading articles:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadMore = async () => {
    setIsLoadingMore(true);
    setShowMore(true);
    
    try {
      await loadCategoryArticles(12);
    } catch (error) {
      console.error('Error loading more articles:', error);
    } finally {
      setIsLoadingMore(false);
    }
  };

  if (isLoading) {
    return (
      <section className="py-8">
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </section>
    );
  }

  if (articles.length === 0) {
    return (
      <section className="py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-foreground">{displayName}</h2>
        </div>
        <div className="text-center py-8">
          <p className="text-muted-foreground">No articles found in this category</p>
        </div>
      </section>
    );
  }

  return (
    <section className="py-12">
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-3xl font-bold text-foreground tracking-tight">{displayName}</h2>
        {!showMore && (
          <Button 
            variant="ghost" 
            onClick={handleLoadMore}
            disabled={isLoadingMore}
            className="text-primary hover:text-primary/80 font-semibold"
          >
            {isLoadingMore ? (
              <>
                <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                Loading...
              </>
            ) : (
              <>
                More <ChevronRight className="h-4 w-4 ml-1" />
              </>
            )}
          </Button>
        )}
      </div>
      
      <div className={`grid gap-6 ${
        showMore 
          ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' 
          : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
      }`}>
        {articles.map((article, index) => (
          <ArticleCard key={article.id || index} article={article} />
        ))}
      </div>
      
      {showMore && (
        <div className="text-center mt-8">
          <Button 
            variant="outline" 
            onClick={() => setShowMore(false)}
            className="font-semibold"
          >
            Show Less
          </Button>
        </div>
      )}
    </section>
  );
}