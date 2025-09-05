import { useState } from 'react';
import { Header } from '@/components/Header';
import { HeroSection } from '@/components/HeroSection';
import { CategorySection } from '@/components/CategorySection';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const { toast } = useToast();

  const categories = [
    { key: 'sports', name: 'Sports & Athletics' },
    { key: 'technology', name: 'Technology & Innovation' },
    { key: 'national', name: 'National News' },
    { key: 'business', name: 'Business & Corporate' },
    { key: 'latest', name: 'Latest News' },
  ];

  const handleLoadMore = async (category: string) => {
    try {
      // This will be handled by CategorySection component
      console.log('Loading more articles for category:', category);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load more articles",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main>
        <HeroSection />
        
        <div className="container mx-auto px-4 space-y-12 pb-16">
          {categories.map((category) => (
            <CategorySection
              key={category.key}
              category={category.key}
              displayName={category.name}
              onLoadMore={handleLoadMore}
            />
          ))}
        </div>
      </main>
    </div>
  );
};

export default Index;
