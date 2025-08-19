"use client";

import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, File, X, CheckCircle, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { apiClient } from "@/lib/api";
import { toast } from "react-hot-toast";
import { formatBytes, getFileExtension, isDocumentFile } from "@/lib/utils";
import { DocumentUploadRequest } from "@/types/document";

interface UploadedFile {
  id: string;
  file: File;
  progress: number;
  status: "uploading" | "processing" | "completed" | "error";
  error?: string;
  documentId?: string;
}

interface DocumentUploadProps {
  onUploadComplete?: (documentId: string) => void;
  className?: string;
}

export function DocumentUpload({ onUploadComplete, className }: DocumentUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = acceptedFiles.map((file) => ({
      id: Math.random().toString(36).substr(2, 9),
      file,
      progress: 0,
      status: "uploading" as const,
    }));

    setUploadedFiles((prev) => [...prev, ...newFiles]);
    handleUpload(newFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "image/*": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"],
      "text/*": [".txt", ".doc", ".docx", ".rtf"],
      "application/msword": [".doc"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: true,
  });

  const handleUpload = async (files: UploadedFile[]) => {
    setIsUploading(true);

    for (const fileData of files) {
      try {
        // Simulate upload progress
        const progressInterval = setInterval(() => {
          setUploadedFiles((prev) =>
            prev.map((f) =>
              f.id === fileData.id
                ? { ...f, progress: Math.min(f.progress + 10, 90) }
                : f
            )
          );
        }, 200);

        // Prepare upload request
        const uploadRequest: DocumentUploadRequest = {
          file: fileData.file,
          metadata: {
            filename: fileData.file.name,
            file_size: fileData.file.size,
            file_type: fileData.file.type,
            uploaded_at: new Date().toISOString(),
          },
        };

        // Upload document
        const response = await apiClient.uploadDocument(uploadRequest);
        
        clearInterval(progressInterval);

        // Update file status
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === fileData.id
              ? {
                  ...f,
                  progress: 100,
                  status: "processing" as const,
                  documentId: response.document_id,
                }
              : f
          )
        );

        toast.success(`Successfully uploaded ${fileData.file.name}`);
        
        if (onUploadComplete && response.document_id) {
          onUploadComplete(response.document_id);
        }

        // Monitor processing status
        monitorProcessingStatus(fileData.id, response.document_id);

      } catch (error) {
        console.error("Upload error:", error);
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === fileData.id
              ? {
                  ...f,
                  status: "error" as const,
                  error: error instanceof Error ? error.message : "Upload failed",
                }
              : f
          )
        );
        toast.error(`Failed to upload ${fileData.file.name}`);
      }
    }

    setIsUploading(false);
  };

  const monitorProcessingStatus = async (fileId: string, documentId: string) => {
    try {
      const status = await apiClient.getDocumentStatus(documentId);
      
      if (status.status === "completed") {
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === fileId
              ? { ...f, status: "completed" as const }
              : f
          )
        );
        toast.success("Document processing completed!");
      } else if (status.status === "failed") {
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === fileId
              ? {
                  ...f,
                  status: "error" as const,
                  error: "Processing failed",
                }
              : f
          )
        );
        toast.error("Document processing failed");
      } else {
        // Continue monitoring
        setTimeout(() => monitorProcessingStatus(fileId, documentId), 2000);
      }
    } catch (error) {
      console.error("Status check error:", error);
    }
  };

  const removeFile = (fileId: string) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== fileId));
  };

  const getStatusIcon = (status: UploadedFile["status"]) => {
    switch (status) {
      case "uploading":
        return <Upload className="h-4 w-4 animate-pulse" />;
      case "processing":
        return <File className="h-4 w-4 animate-spin" />;
      case "completed":
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "error":
        return <AlertCircle className="h-4 w-4 text-red-500" />;
    }
  };

  const getStatusColor = (status: UploadedFile["status"]) => {
    switch (status) {
      case "uploading":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "processing":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "completed":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "error":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
    }
  };

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Upload Documents
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Drop Zone */}
          <div
            {...getRootProps()}
            className={`
              border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
              ${isDragActive
                ? "border-primary bg-primary/5"
                : "border-muted-foreground/25 hover:border-primary/50"
              }
            `}
          >
            <input {...getInputProps()} />
            <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-lg font-medium mb-2">
              {isDragActive ? "Drop files here" : "Drag & drop files here"}
            </p>
            <p className="text-sm text-muted-foreground mb-4">
              or click to select files
            </p>
            <div className="flex flex-wrap gap-2 justify-center">
              <Badge variant="secondary">PDF</Badge>
              <Badge variant="secondary">Images</Badge>
              <Badge variant="secondary">Word Docs</Badge>
              <Badge variant="secondary">Text Files</Badge>
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Max file size: 50MB
            </p>
          </div>

          {/* Upload Progress */}
          {uploadedFiles.length > 0 && (
            <div className="space-y-3">
              <h3 className="font-medium">Upload Progress</h3>
              {uploadedFiles.map((fileData) => (
                <div
                  key={fileData.id}
                  className="border rounded-lg p-4 space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {getStatusIcon(fileData.status)}
                      <div>
                        <p className="font-medium text-sm">
                          {fileData.file.name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {formatBytes(fileData.file.size)} • {getFileExtension(fileData.file.name)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge className={getStatusColor(fileData.status)}>
                        {fileData.status}
                      </Badge>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(fileData.id)}
                        className="h-6 w-6 p-0"
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>

                  <Progress value={fileData.progress} className="h-2" />

                  {fileData.error && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>{fileData.error}</AlertDescription>
                    </Alert>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Upload Button */}
          {uploadedFiles.length === 0 && (
            <Button
              onClick={() => document.querySelector('input[type="file"]')?.click()}
              disabled={isUploading}
              className="w-full"
            >
              {isUploading ? "Uploading..." : "Select Files"}
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
