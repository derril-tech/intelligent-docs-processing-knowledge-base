"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Search, Filter, BookOpen, FileText, Calendar, User, Tag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Skeleton } from "@/components/ui/skeleton";
import { apiClient } from "@/lib/api";
import { toast } from "react-hot-toast";
import { formatDate, truncateText } from "@/lib/utils";
import { KnowledgeEntry, Document } from "@/types/document";
import { useDebounce } from "@/hooks/use-debounce";

interface SearchFilters {
  documentType: string[];
  dateRange: string;
  author: string[];
  tags: string[];
  status: string[];
}

interface KnowledgeBaseSearchProps {
  onResultSelect?: (entry: KnowledgeEntry) => void;
  className?: string;
}

export function KnowledgeBaseSearch({ onResultSelect, className }: KnowledgeBaseSearchProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<SearchFilters>({
    documentType: [],
    dateRange: "",
    author: [],
    tags: [],
    status: [],
  });
  const [results, setResults] = useState<KnowledgeEntry[]>([]);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("knowledge");
  const [showFilters, setShowFilters] = useState(false);

  const debouncedSearchQuery = useDebounce(searchQuery, 300);

  // Available filter options
  const documentTypes = ["PDF", "Image", "Word", "Text", "Spreadsheet"];
  const dateRanges = ["Last 24 hours", "Last 7 days", "Last 30 days", "Last 3 months", "All time"];
  const statuses = ["Processed", "Processing", "Failed", "Pending Review"];

  useEffect(() => {
    if (debouncedSearchQuery || Object.values(filters).some(f => Array.isArray(f) ? f.length > 0 : f !== "")) {
      performSearch();
    }
  }, [debouncedSearchQuery, filters]);

  const performSearch = async () => {
    setIsLoading(true);
    try {
      if (activeTab === "knowledge") {
        const searchResults = await apiClient.searchKnowledgeBase({
          query: debouncedSearchQuery,
          filters: {
            document_types: filters.documentType,
            date_range: filters.dateRange,
            authors: filters.author,
            tags: filters.tags,
            statuses: filters.status,
          },
          limit: 50,
        });
        setResults(searchResults.entries);
      } else {
        const documentResults = await apiClient.getDocuments({
          search: debouncedSearchQuery,
          document_type: filters.documentType,
          status: filters.status,
          limit: 50,
        });
        setDocuments(documentResults.documents);
      }
    } catch (error) {
      console.error("Search error:", error);
      toast.error("Failed to perform search");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (filterType: keyof SearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value,
    }));
  };

  const clearFilters = () => {
    setFilters({
      documentType: [],
      dateRange: "",
      author: [],
      tags: [],
      status: [],
    });
  };

  const handleResultClick = (entry: KnowledgeEntry) => {
    if (onResultSelect) {
      onResultSelect(entry);
    }
  };

  const renderKnowledgeResult = (entry: KnowledgeEntry) => (
    <Card 
      key={entry.id} 
      className="cursor-pointer hover:shadow-md transition-shadow"
      onClick={() => handleResultClick(entry)}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-muted-foreground" />
            <span className="font-medium text-sm">{entry.document_title}</span>
          </div>
          <Badge variant="secondary" className="text-xs">
            {entry.confidence_score}% match
          </Badge>
        </div>
        
        <p className="text-sm text-muted-foreground mb-3">
          {truncateText(entry.content, 200)}
        </p>
        
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            {formatDate(entry.created_at)}
          </div>
          <div className="flex items-center gap-1">
            <User className="h-3 w-3" />
            {entry.author || "Unknown"}
          </div>
          <div className="flex items-center gap-1">
            <Tag className="h-3 w-3" />
            {entry.document_type}
          </div>
        </div>
        
        {entry.tags && entry.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {entry.tags.slice(0, 3).map((tag, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}
            {entry.tags.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{entry.tags.length - 3} more
              </Badge>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );

  const renderDocumentResult = (document: Document) => (
    <Card 
      key={document.id} 
      className="cursor-pointer hover:shadow-md transition-shadow"
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2">
            <FileText className="h-4 w-4 text-muted-foreground" />
            <span className="font-medium text-sm">{document.filename}</span>
          </div>
          <Badge 
            variant={document.status === "completed" ? "default" : "secondary"}
            className="text-xs"
          >
            {document.status}
          </Badge>
        </div>
        
        <p className="text-sm text-muted-foreground mb-3">
          {document.metadata?.description || "No description available"}
        </p>
        
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            {formatDate(document.uploaded_at)}
          </div>
          <div className="flex items-center gap-1">
            <User className="h-3 w-3" />
            {document.uploaded_by || "Unknown"}
          </div>
          <div className="flex items-center gap-1">
            <Tag className="h-3 w-3" />
            {document.document_type}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Knowledge Base Search
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Search Input */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search knowledge base..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="knowledge">Knowledge Entries</TabsTrigger>
              <TabsTrigger value="documents">Documents</TabsTrigger>
            </TabsList>
          </Tabs>

          {/* Filters */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center gap-2"
              >
                <Filter className="h-4 w-4" />
                Filters
              </Button>
              {(Object.values(filters).some(f => Array.isArray(f) ? f.length > 0 : f !== "")) && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearFilters}
                >
                  Clear All
                </Button>
              )}
            </div>

            {showFilters && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4 border rounded-lg bg-muted/50">
                {/* Document Type Filter */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Document Type</label>
                  <div className="space-y-2">
                    {documentTypes.map((type) => (
                      <div key={type} className="flex items-center space-x-2">
                        <Checkbox
                          id={`type-${type}`}
                          checked={filters.documentType.includes(type)}
                          onCheckedChange={(checked) => {
                            const newTypes = checked
                              ? [...filters.documentType, type]
                              : filters.documentType.filter(t => t !== type);
                            handleFilterChange("documentType", newTypes);
                          }}
                        />
                        <label htmlFor={`type-${type}`} className="text-sm">
                          {type}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Date Range Filter */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Date Range</label>
                  <Select
                    value={filters.dateRange}
                    onValueChange={(value) => handleFilterChange("dateRange", value)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select date range" />
                    </SelectTrigger>
                    <SelectContent>
                      {dateRanges.map((range) => (
                        <SelectItem key={range} value={range}>
                          {range}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Status Filter */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Status</label>
                  <div className="space-y-2">
                    {statuses.map((status) => (
                      <div key={status} className="flex items-center space-x-2">
                        <Checkbox
                          id={`status-${status}`}
                          checked={filters.status.includes(status)}
                          onCheckedChange={(checked) => {
                            const newStatuses = checked
                              ? [...filters.status, status]
                              : filters.status.filter(s => s !== status);
                            handleFilterChange("status", newStatuses);
                          }}
                        />
                        <label htmlFor={`status-${status}`} className="text-sm">
                          {status}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Results */}
          <div className="space-y-3">
            {isLoading ? (
              // Loading skeletons
              Array.from({ length: 3 }).map((_, index) => (
                <Card key={index}>
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <Skeleton className="h-4 w-32" />
                      <Skeleton className="h-4 w-16" />
                    </div>
                    <Skeleton className="h-4 w-full mb-2" />
                    <Skeleton className="h-4 w-3/4 mb-3" />
                    <div className="flex gap-4">
                      <Skeleton className="h-3 w-20" />
                      <Skeleton className="h-3 w-16" />
                      <Skeleton className="h-3 w-24" />
                    </div>
                  </CardContent>
                </Card>
              ))
            ) : activeTab === "knowledge" ? (
              results.length > 0 ? (
                <div className="space-y-3">
                  <p className="text-sm text-muted-foreground">
                    Found {results.length} knowledge entries
                  </p>
                  {results.map(renderKnowledgeResult)}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <BookOpen className="mx-auto h-12 w-12 mb-4 opacity-50" />
                  <p>No knowledge entries found</p>
                  <p className="text-sm">Try adjusting your search terms or filters</p>
                </div>
              )
            ) : (
              documents.length > 0 ? (
                <div className="space-y-3">
                  <p className="text-sm text-muted-foreground">
                    Found {documents.length} documents
                  </p>
                  {documents.map(renderDocumentResult)}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <FileText className="mx-auto h-12 w-12 mb-4 opacity-50" />
                  <p>No documents found</p>
                  <p className="text-sm">Try adjusting your search terms or filters</p>
                </div>
              )
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
