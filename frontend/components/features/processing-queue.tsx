"use client";

import React, { useState, useEffect } from "react";
import { Clock, CheckCircle, AlertCircle, Play, Pause, RefreshCw, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { apiClient } from "@/lib/api";
import { toast } from "react-hot-toast";
import { formatDate, formatBytes, getStatusColor } from "@/lib/utils";
import { ProcessingTask, ProcessingStatus } from "@/types/document";
import { useWebSocket } from "@/app/providers/websocket-provider";

interface ProcessingQueueProps {
  className?: string;
}

export function ProcessingQueue({ className }: ProcessingQueueProps) {
  const [tasks, setTasks] = useState<ProcessingTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("all");
  const { socket } = useWebSocket();

  useEffect(() => {
    loadProcessingTasks();
    
    // Set up WebSocket listeners for real-time updates
    if (socket) {
      socket.on("document_processed", handleDocumentProcessed);
      socket.on("processing_task_updated", handleTaskUpdated);
      socket.on("processing_task_failed", handleTaskFailed);
    }

    return () => {
      if (socket) {
        socket.off("document_processed", handleDocumentProcessed);
        socket.off("processing_task_updated", handleTaskUpdated);
        socket.off("processing_task_failed", handleTaskFailed);
      }
    };
  }, [socket]);

  const loadProcessingTasks = async () => {
    try {
      setIsLoading(true);
      const response = await apiClient.getProcessingTasks();
      setTasks(response.tasks);
    } catch (error) {
      console.error("Failed to load processing tasks:", error);
      toast.error("Failed to load processing queue");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDocumentProcessed = (data: { task_id: string; document_id: string }) => {
    setTasks(prev => prev.map(task => 
      task.id === data.task_id 
        ? { ...task, status: "completed" as ProcessingStatus, progress: 100 }
        : task
    ));
    toast.success("Document processing completed!");
  };

  const handleTaskUpdated = (data: { task_id: string; progress: number; status: ProcessingStatus }) => {
    setTasks(prev => prev.map(task => 
      task.id === data.task_id 
        ? { ...task, progress: data.progress, status: data.status }
        : task
    ));
  };

  const handleTaskFailed = (data: { task_id: string; error: string }) => {
    setTasks(prev => prev.map(task => 
      task.id === data.task_id 
        ? { ...task, status: "failed" as ProcessingStatus, error: data.error }
        : task
    ));
    toast.error(`Processing failed: ${data.error}`);
  };

  const handleRetryTask = async (taskId: string) => {
    try {
      await apiClient.retryProcessingTask(taskId);
      toast.success("Task queued for retry");
      loadProcessingTasks(); // Refresh the list
    } catch (error) {
      console.error("Failed to retry task:", error);
      toast.error("Failed to retry task");
    }
  };

  const handleCancelTask = async (taskId: string) => {
    try {
      await apiClient.cancelProcessingTask(taskId);
      toast.success("Task cancelled");
      loadProcessingTasks(); // Refresh the list
    } catch (error) {
      console.error("Failed to cancel task:", error);
      toast.error("Failed to cancel task");
    }
  };

  const getFilteredTasks = () => {
    switch (activeTab) {
      case "active":
        return tasks.filter(task => ["pending", "processing"].includes(task.status));
      case "completed":
        return tasks.filter(task => task.status === "completed");
      case "failed":
        return tasks.filter(task => task.status === "failed");
      default:
        return tasks;
    }
  };

  const getStatusIcon = (status: ProcessingStatus) => {
    switch (status) {
      case "pending":
        return <Clock className="h-4 w-4 text-yellow-500" />;
      case "processing":
        return <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />;
      case "completed":
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "failed":
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4 text-muted-foreground" />;
    }
  };

  const getStatusBadge = (status: ProcessingStatus) => {
    const colors = getStatusColor(status);
    return (
      <Badge className={colors}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    );
  };

  const getActionButtons = (task: ProcessingTask) => {
    switch (task.status) {
      case "pending":
        return (
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleCancelTask(task.id)}
            className="h-8"
          >
            <X className="h-3 w-3 mr-1" />
            Cancel
          </Button>
        );
      case "processing":
        return (
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleCancelTask(task.id)}
            className="h-8"
          >
            <Pause className="h-3 w-3 mr-1" />
            Cancel
          </Button>
        );
      case "failed":
        return (
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleRetryTask(task.id)}
            className="h-8"
          >
            <RefreshCw className="h-3 w-3 mr-1" />
            Retry
          </Button>
        );
      default:
        return null;
    }
  };

  const filteredTasks = getFilteredTasks();
  const stats = {
    total: tasks.length,
    active: tasks.filter(t => ["pending", "processing"].includes(t.status)).length,
    completed: tasks.filter(t => t.status === "completed").length,
    failed: tasks.filter(t => t.status === "failed").length,
  };

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <RefreshCw className="h-5 w-5" />
              Processing Queue
            </CardTitle>
            <Button
              variant="outline"
              size="sm"
              onClick={loadProcessingTasks}
              disabled={isLoading}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`} />
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Stats Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Total</span>
                </div>
                <p className="text-2xl font-bold">{stats.total}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <Play className="h-4 w-4 text-blue-500" />
                  <span className="text-sm font-medium">Active</span>
                </div>
                <p className="text-2xl font-bold text-blue-600">{stats.active}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  <span className="text-sm font-medium">Completed</span>
                </div>
                <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 text-red-500" />
                  <span className="text-sm font-medium">Failed</span>
                </div>
                <p className="text-2xl font-bold text-red-600">{stats.failed}</p>
              </CardContent>
            </Card>
          </div>

          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="all">All ({stats.total})</TabsTrigger>
              <TabsTrigger value="active">Active ({stats.active})</TabsTrigger>
              <TabsTrigger value="completed">Completed ({stats.completed})</TabsTrigger>
              <TabsTrigger value="failed">Failed ({stats.failed})</TabsTrigger>
            </TabsList>
          </Tabs>

          {/* Tasks Table */}
          <div className="border rounded-lg">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Document</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Progress</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  // Loading skeleton rows
                  Array.from({ length: 5 }).map((_, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <div className="space-y-2">
                          <div className="h-4 bg-muted rounded animate-pulse" />
                          <div className="h-3 bg-muted rounded w-3/4 animate-pulse" />
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="h-4 bg-muted rounded w-16 animate-pulse" />
                      </TableCell>
                      <TableCell>
                        <div className="h-6 bg-muted rounded w-20 animate-pulse" />
                      </TableCell>
                      <TableCell>
                        <div className="h-2 bg-muted rounded animate-pulse" />
                      </TableCell>
                      <TableCell>
                        <div className="h-4 bg-muted rounded w-24 animate-pulse" />
                      </TableCell>
                      <TableCell>
                        <div className="h-8 bg-muted rounded w-16 animate-pulse" />
                      </TableCell>
                    </TableRow>
                  ))
                ) : filteredTasks.length > 0 ? (
                  filteredTasks.map((task) => (
                    <TableRow key={task.id}>
                      <TableCell>
                        <div>
                          <p className="font-medium text-sm">{task.document.filename}</p>
                          <p className="text-xs text-muted-foreground">
                            {formatBytes(task.document.file_size)}
                          </p>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className="text-xs">
                          {task.document.document_type}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(task.status)}
                          {getStatusBadge(task.status)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="w-24">
                          <Progress value={task.progress} className="h-2" />
                          <p className="text-xs text-muted-foreground mt-1">
                            {task.progress}%
                          </p>
                        </div>
                      </TableCell>
                      <TableCell>
                        <p className="text-sm">{formatDate(task.created_at)}</p>
                      </TableCell>
                      <TableCell>
                        {getActionButtons(task)}
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8">
                      <div className="text-muted-foreground">
                        <RefreshCw className="mx-auto h-12 w-12 mb-4 opacity-50" />
                        <p>No tasks found</p>
                        <p className="text-sm">
                          {activeTab === "all" 
                            ? "No processing tasks available"
                            : `No ${activeTab} tasks found`
                          }
                        </p>
                      </div>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>

          {/* Error Display */}
          {filteredTasks.some(task => task.error) && (
            <div className="space-y-2">
              <h4 className="font-medium text-sm">Recent Errors</h4>
              {filteredTasks
                .filter(task => task.error)
                .slice(0, 3)
                .map((task) => (
                  <div key={task.id} className="p-3 border border-red-200 rounded-lg bg-red-50 dark:bg-red-950 dark:border-red-800">
                    <div className="flex items-start gap-2">
                      <AlertCircle className="h-4 w-4 text-red-500 mt-0.5" />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-red-800 dark:text-red-200">
                          {task.document.filename}
                        </p>
                        <p className="text-xs text-red-600 dark:text-red-300">
                          {task.error}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
