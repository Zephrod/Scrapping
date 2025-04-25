namespace Scrapper;

public class Article
{
    public required string Title { get; set; }
    public required string Url { get; set; }
    public required string Section { get; set; }
    public required string Content { get; set; }
    public DateTime ScrapedAt { get; set; }
}
