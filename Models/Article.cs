using System.Text.Json.Serialization;

namespace Scrapper;

public class Article
{
    [JsonPropertyName("title")]
    public required string Title { get; set; }
    
    [JsonPropertyName("url")]
    public required string Url { get; set; }
    
    [JsonPropertyName("section")]
    public required string Section { get; set; }
    
    [JsonPropertyName("content")]
    public required string Content { get; set; }
    [JsonPropertyName("summary")]
    public required string Summary { get; set; }
}
