using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Scrapper.Models;

namespace Scrapper.Controllers;

public class HomeController : Controller
{
    private readonly ArticleService _articleService;

    public HomeController(ArticleService articleService)
    {
        _articleService = articleService;
    }

    public IActionResult Index(string searchQuery)
{
    var articles = _articleService.GetArticles(searchQuery);
    Console.WriteLine($"Found {articles.Count} articles"); // Check debug output
    return View(articles);
}
}