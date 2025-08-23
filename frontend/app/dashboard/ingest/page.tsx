'use client';

import { useState, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Upload,
  FileText,
  Cloud,
  Database,
  Settings,
  CheckCircle,
  AlertCircle,
  Clock,
  X,
  Plus,
  ExternalLink,
  Eye,
  EyeOff,
  Download,
  RefreshCw
} from 'lucide-react';
import { apiClient } from '@/lib/api';

interface UploadFile {
  id: string;
  name: string;
  size: number;
  type: string;
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'failed';
  progress: number;
  error?: string;
  uploaded_at?: Date;
  processing_started_at?: Date;
  completed_at?: Date;
}

interface Connector {
  id: string;
  name: string;
  type: 's3' | 'gdrive' | 'sharepoint' | 'confluence' | 'github' | 'slack';
  status: 'connected' | 'disconnected' | 'error';
  last_sync?: Date;
  documents_count: number;
  icon: React.ComponentType<any>;
}

export default function IngestStudioPage() {
  const [files, setFiles] = useState<UploadFile[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadSettings, setUploadSettings] = useState({
    enableOCR: true,
    enablePII: false,
    enableLayoutParsing: true,
    chunkSize: 'medium',
    knowledgeBase: 'general',
    tags: [] as string[],
    metadata: {} as Record<string, string>
  });
  const [activeTab, setActiveTab] = useState('upload');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const connectors: Connector[] = [
    {
      id: 's3',
      name: 'Amazon S3',
      type: 's3',
      status: 'connected',
      last_sync: new Date(Date.now() - 24 * 60 * 60 * 1000),
      documents_count: 1250,
      icon: Cloud
    },
    {
      id: 'gdrive',
      name: 'Google Drive',
      type: 'gdrive',
      status: 'connected',
      last_sync: new Date(Date.now() - 2 * 60 * 60 * 1000),
      documents_count: 890,
      icon: Cloud
    },
    {
      id: 'sharepoint',
      name: 'SharePoint',
      type: 'sharepoint',
      status: 'disconnected',
      documents_count: 0,
      icon: Database
    },
    {
      id: 'confluence',
      name: 'Confluence',
      type: 'confluence',
      status: 'error',
      last_sync: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      documents_count: 340,
      icon: ExternalLink
    }
  ];

  const handleFileSelect = (selectedFiles: FileList | null) => {
    if (!selectedFiles) return;

    const newFiles: UploadFile[] = Array.from(selectedFiles).map(file => ({
      id: Date.now() + Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'pending',
      progress: 0
    }));

    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const uploadFiles = async () => {
    const pendingFiles = files.filter(file => file.status === 'pending');
    
    for (const file of pendingFiles) {
      // Update status to uploading
      setFiles(prev => prev.map(f => 
        f.id === file.id ? { ...f, status: 'uploading' as const } : f
      ));

      try {
        // Simulate upload progress
        for (let progress = 0; progress <= 100; progress += 10) {
          await new Promise(resolve => setTimeout(resolve, 100));
          setFiles(prev => prev.map(f => 
            f.id === file.id ? { ...f, progress } : f
          ));
        }

        // Update status to processing
        setFiles(prev => prev.map(f => 
          f.id === file.id ? { 
            ...f, 
            status: 'processing' as const, 
            uploaded_at: new Date(),
            processing_started_at: new Date()
          } : f
        ));

        // Simulate processing
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Update status to completed
        setFiles(prev => prev.map(f => 
          f.id === file.id ? { 
            ...f, 
            status: 'completed' as const,
            completed_at: new Date()
          } : f
        ));

      } catch (error) {
        setFiles(prev => prev.map(f => 
          f.id === file.id ? { 
            ...f, 
            status: 'failed' as const,
            error: 'Upload failed'
          } : f
        ));
      }
    }
  };

  const syncConnector = async (connectorId: string) => {
    // TODO: Implement connector sync
    console.log('Syncing connector:', connectorId);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusIcon = (status: UploadFile['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      case 'processing':
        return <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />;
      case 'uploading':
        return <Clock className="h-4 w-4 text-yellow-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: UploadFile['status']) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      case 'processing':
        return 'text-blue-600 bg-blue-50';
      case 'uploading':
        return 'text-yellow-600 bg-yellow-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Ingest Studio
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Upload documents and connect external sources to build your knowledge base
          </p>
        </div>
        <Button onClick={() => setActiveTab('settings')}>
          <Settings className="h-4 w-4 mr-2" />
          Settings
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="upload">Upload Files</TabsTrigger>
          <TabsTrigger value="connectors">Connectors</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="space-y-6">
          {/* Upload Area */}
          <Card>
            <CardHeader>
              <CardTitle>Upload Documents</CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  isDragOver 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-300 hover:border-gray-400'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
              >
                <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  Drop files here or click to browse
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  Support for PDF, DOCX, TXT, CSV, and image files up to 100MB each
                </p>
                <Button onClick={() => fileInputRef.current?.click()}>
                  <Plus className="h-4 w-4 mr-2" />
                  Select Files
                </Button>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".pdf,.docx,.txt,.csv,.png,.jpg,.jpeg"
                  onChange={(e) => handleFileSelect(e.target.files)}
                  className="hidden"
                />
              </div>
            </CardContent>
          </Card>

          {/* File List */}
          {files.length > 0 && (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Upload Queue ({files.length})</CardTitle>
                  <Button onClick={uploadFiles} disabled={!files.some(f => f.status === 'pending')}>
                    <Upload className="h-4 w-4 mr-2" />
                    Upload All
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {files.map((file) => (
                    <div key={file.id} className="flex items-center space-x-4 p-4 border rounded-lg">
                      <div className="flex-shrink-0">
                        {getStatusIcon(file.status)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                              {file.name}
                            </p>
                            <p className="text-sm text-gray-500">
                              {formatFileSize(file.size)} • {file.type}
                            </p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge className={getStatusColor(file.status)}>
                              {file.status}
                            </Badge>
                            {file.status !== 'pending' && (
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => removeFile(file.id)}
                              >
                                <X className="h-4 w-4" />
                              </Button>
                            )}
                          </div>
                        </div>
                        {file.status !== 'pending' && (
                          <Progress value={file.progress} className="mt-2" />
                        )}
                        {file.error && (
                          <p className="text-sm text-red-600 mt-1">{file.error}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="connectors" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>External Connectors</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {connectors.map((connector) => {
                  const Icon = connector.icon;
                  return (
                    <div key={connector.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="flex-shrink-0">
                          <Icon className="h-8 w-8 text-gray-400" />
                        </div>
                        <div>
                          <h3 className="text-sm font-medium text-gray-900 dark:text-white">
                            {connector.name}
                          </h3>
                          <p className="text-sm text-gray-500">
                            {connector.documents_count} documents
                            {connector.last_sync && (
                              <span> • Last sync: {connector.last_sync.toLocaleDateString()}</span>
                            )}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge 
                          variant={connector.status === 'connected' ? 'default' : 
                                  connector.status === 'error' ? 'destructive' : 'secondary'}
                        >
                          {connector.status}
                        </Badge>
                        {connector.status === 'connected' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => syncConnector(connector.id)}
                          >
                            <RefreshCw className="h-4 w-4 mr-2" />
                            Sync
                          </Button>
                        )}
                        {connector.status === 'disconnected' && (
                          <Button size="sm">
                            Connect
                          </Button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Upload Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid gap-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-medium">Processing Options</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <label className="text-sm font-medium">Enable OCR</label>
                        <p className="text-sm text-gray-500">Extract text from images and scanned documents</p>
                      </div>
                      <Switch
                        checked={uploadSettings.enableOCR}
                        onCheckedChange={(checked) => 
                          setUploadSettings(prev => ({ ...prev, enableOCR: checked }))
                        }
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <label className="text-sm font-medium">PII Detection</label>
                        <p className="text-sm text-gray-500">Automatically detect and redact sensitive information</p>
                      </div>
                      <Switch
                        checked={uploadSettings.enablePII}
                        onCheckedChange={(checked) => 
                          setUploadSettings(prev => ({ ...prev, enablePII: checked }))
                        }
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <label className="text-sm font-medium">Layout Parsing</label>
                        <p className="text-sm text-gray-500">Preserve document structure and formatting</p>
                      </div>
                      <Switch
                        checked={uploadSettings.enableLayoutParsing}
                        onCheckedChange={(checked) => 
                          setUploadSettings(prev => ({ ...prev, enableLayoutParsing: checked }))
                        }
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-medium">Chunking Settings</h3>
                  <div>
                    <label className="block text-sm font-medium mb-2">Chunk Size</label>
                    <select 
                      className="w-full p-2 border rounded-md"
                      value={uploadSettings.chunkSize}
                      onChange={(e) => 
                        setUploadSettings(prev => ({ ...prev, chunkSize: e.target.value }))
                      }
                    >
                      <option value="small">Small (256 tokens)</option>
                      <option value="medium">Medium (512 tokens)</option>
                      <option value="large">Large (1024 tokens)</option>
                    </select>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-medium">Default Settings</h3>
                  <div>
                    <label className="block text-sm font-medium mb-2">Knowledge Base</label>
                    <select 
                      className="w-full p-2 border rounded-md"
                      value={uploadSettings.knowledgeBase}
                      onChange={(e) => 
                        setUploadSettings(prev => ({ ...prev, knowledgeBase: e.target.value }))
                      }
                    >
                      <option value="general">General Documents</option>
                      <option value="legal">Legal Documents</option>
                      <option value="technical">Technical Documentation</option>
                    </select>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
