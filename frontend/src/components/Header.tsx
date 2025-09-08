import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';

export function Header() {
  const [isHealthy, setIsHealthy] = useState(true);

  useEffect(() => {
    checkApiHealth();
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch('https://newssummariser-5a49.onrender.com/', {
        method: 'GET',
      });
      setIsHealthy(response.ok);
    } catch {
      setIsHealthy(false);
    }
  };

  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 flex items-center justify-between h-20">
        <div className="flex items-center gap-3">
          <div className="text-3xl font-bold text-news-brand tracking-tight">
            DailyNews AI
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isHealthy ? 'bg-green-500' : 'bg-red-500'} shadow-sm`} />
            <span className="text-xs text-muted-foreground font-medium">
              {isHealthy ? 'API Online' : 'API Offline'}
            </span>
          </div>
        </div>
        
        <nav className="hidden md:flex items-center space-x-8">
          <Button variant="ghost" className="text-foreground hover:text-primary font-medium">
            Home
          </Button>
          <Button variant="ghost" className="text-foreground hover:text-primary font-medium">
            About
          </Button>
        </nav>
      </div>
    </header>
  );
}