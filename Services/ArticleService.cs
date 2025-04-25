using System.Text.Json;

namespace Scrapper;

public class ArticleService
{
    private readonly IWebHostEnvironment _env;
    
    public ArticleService(IWebHostEnvironment env)
    {
        _env = env;
    }

    public List<Article> GetArticles(string? searchTerm = null)
    {
        var path = Path.Combine(_env.WebRootPath, "articles.json");
        
        if (!File.Exists(path))
            return new List<Article>();

        var json = File.ReadAllText(path);
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            AllowTrailingCommas = true
        };

var articles = JsonSerializer.Deserialize<List<Article>>(json, options) ?? new List<Article>();

        return string.IsNullOrEmpty(searchTerm) 
            ? articles 
            : articles.Where(a => 
                (a.Title?.Contains(searchTerm, StringComparison.OrdinalIgnoreCase) ?? false) ||
                (a.Content?.Contains(searchTerm, StringComparison.OrdinalIgnoreCase) ?? false)
              ).ToList();
    }
}