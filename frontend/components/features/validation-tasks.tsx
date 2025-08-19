"use client";

import React, { useState, useEffect } from "react";
import { CheckCircle, XCircle, Clock, AlertCircle, Eye, Check, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/modal";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { apiClient } from "@/lib/api";
import { toast } from "react-hot-toast";
import { formatDate, getStatusColor } from "@/lib/utils";
import { ValidationTask, ValidationStatus } from "@/types/validation";
import { useWebSocket } from "@/app/providers/websocket-provider";

interface ValidationTasksProps {
  className?: string;
}

interface ValidationModalProps {
  task: ValidationTask;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (taskId: string, result: any) => void;
}

function ValidationModal({ task, isOpen, onClose, onSubmit }: ValidationModalProps) {
  const [validation, setValidation] = useState("");
  const [confidence, setConfidence] = useState("");
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!validation || !confidence) {
      toast.error("Please provide validation result and confidence level");
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(task.id, {
        validation_result: validation,
        confidence_level: confidence,
        notes: notes,
      });
      onClose();
      setValidation("");
      setConfidence("");
      setNotes("");
    } catch (error) {
      console.error("Validation submission error:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Validate Extraction: {task.document.filename}</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-6">
          {/* Original Document Info */}
          <div className="p-4 border rounded-lg bg-muted/50">
            <h3 className="font-medium mb-2">Document Information</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Document:</span>
                <p className="font-medium">{task.document.filename}</p>
              </div>
              <div>
                <span className="text-muted-foreground">Type:</span>
                <p className="font-medium">{task.document.document_type}</p>
              </div>
              <div>
                <span className="text-muted-foreground">Field:</span>
                <p className="font-medium">{task.field_name}</p>
              </div>
              <div>
                <span className="text-muted-foreground">Confidence:</span>
                <p className="font-medium">{task.ai_confidence}%</p>
              </div>
            </div>
          </div>

          {/* AI Extraction Result */}
          <div className="p-4 border rounded-lg">
            <h3 className="font-medium mb-2">AI Extraction Result</h3>
            <div className="p-3 bg-muted rounded">
              <p className="text-sm">{task.extracted_value || "No value extracted"}</p>
            </div>
          </div>

          {/* Validation Form */}
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">
                Is this extraction correct?
              </label>
              <RadioGroup value={validation} onValueChange={setValidation}>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="correct" id="correct" />
                  <label htmlFor="correct" className="text-sm">Correct</label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="incorrect" id="incorrect" />
                  <label htmlFor="incorrect" className="text-sm">Incorrect</label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="partially_correct" id="partially" />
                  <label htmlFor="partially" className="text-sm">Partially Correct</label>
                </div>
              </RadioGroup>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">
                Confidence Level
              </label>
              <RadioGroup value={confidence} onValueChange={setConfidence}>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="high" id="high" />
                  <label htmlFor="high" className="text-sm">High (90-100%)</label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="medium" id="medium" />
                  <label htmlFor="medium" className="text-sm">Medium (70-89%)</label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="low" id="low" />
                  <label htmlFor="low" className="text-sm">Low (50-69%)</label>
                </div>
              </RadioGroup>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">
                Notes (Optional)
              </label>
              <Textarea
                placeholder="Add any additional notes or corrections..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button 
              onClick={handleSubmit} 
              disabled={isSubmitting || !validation || !confidence}
            >
              {isSubmitting ? "Submitting..." : "Submit Validation"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

export function ValidationTasks({ className }: ValidationTasksProps) {
  const [tasks, setTasks] = useState<ValidationTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("pending");
  const [selectedTask, setSelectedTask] = useState<ValidationTask | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { socket } = useWebSocket();

  useEffect(() => {
    loadValidationTasks();
    
    // Set up WebSocket listeners for real-time updates
    if (socket) {
      socket.on("validation_task_updated", handleTaskUpdated);
      socket.on("validation_task_assigned", handleTaskAssigned);
    }

    return () => {
      if (socket) {
        socket.off("validation_task_updated", handleTaskUpdated);
        socket.off("validation_task_assigned", handleTaskAssigned);
      }
    };
  }, [socket]);

  const loadValidationTasks = async () => {
    try {
      setIsLoading(true);
      const response = await apiClient.getMyValidationTasks();
      setTasks(response.tasks);
    } catch (error) {
      console.error("Failed to load validation tasks:", error);
      toast.error("Failed to load validation tasks");
    } finally {
      setIsLoading(false);
    }
  };

  const handleTaskUpdated = (data: { task_id: string; status: ValidationStatus }) => {
    setTasks(prev => prev.map(task => 
      task.id === data.task_id 
        ? { ...task, status: data.status }
        : task
    ));
  };

  const handleTaskAssigned = (data: { task_id: string; assigned_to: string }) => {
    // Refresh the list when new tasks are assigned
    loadValidationTasks();
  };

  const handleAssignTask = async (taskId: string) => {
    try {
      await apiClient.assignValidationTask(taskId);
      toast.success("Task assigned successfully");
      loadValidationTasks();
    } catch (error) {
      console.error("Failed to assign task:", error);
      toast.error("Failed to assign task");
    }
  };

  const handleSubmitValidation = async (taskId: string, result: any) => {
    try {
      await apiClient.submitValidationResult(taskId, result);
      toast.success("Validation submitted successfully");
      loadValidationTasks();
    } catch (error) {
      console.error("Failed to submit validation:", error);
      toast.error("Failed to submit validation");
      throw error;
    }
  };

  const getFilteredTasks = () => {
    switch (activeTab) {
      case "pending":
        return tasks.filter(task => task.status === "pending");
      case "in_progress":
        return tasks.filter(task => task.status === "in_progress");
      case "completed":
        return tasks.filter(task => task.status === "completed");
      case "rejected":
        return tasks.filter(task => task.status === "rejected");
      default:
        return tasks;
    }
  };

  const getStatusIcon = (status: ValidationStatus) => {
    switch (status) {
      case "pending":
        return <Clock className="h-4 w-4 text-yellow-500" />;
      case "in_progress":
        return <AlertCircle className="h-4 w-4 text-blue-500" />;
      case "completed":
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "rejected":
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4 text-muted-foreground" />;
    }
  };

  const getStatusBadge = (status: ValidationStatus) => {
    const colors = getStatusColor(status);
    return (
      <Badge className={colors}>
        {status.replace("_", " ").charAt(0).toUpperCase() + status.replace("_", " ").slice(1)}
      </Badge>
    );
  };

  const getActionButtons = (task: ValidationTask) => {
    switch (task.status) {
      case "pending":
        return (
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleAssignTask(task.id)}
            className="h-8"
          >
            <Check className="h-3 w-3 mr-1" />
            Assign
          </Button>
        );
      case "in_progress":
        return (
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setSelectedTask(task);
              setIsModalOpen(true);
            }}
            className="h-8"
          >
            <Eye className="h-3 w-3 mr-1" />
            Validate
          </Button>
        );
      default:
        return null;
    }
  };

  const filteredTasks = getFilteredTasks();
  const stats = {
    total: tasks.length,
    pending: tasks.filter(t => t.status === "pending").length,
    in_progress: tasks.filter(t => t.status === "in_progress").length,
    completed: tasks.filter(t => t.status === "completed").length,
    rejected: tasks.filter(t => t.status === "rejected").length,
  };

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5" />
              Validation Tasks
            </CardTitle>
            <Button
              variant="outline"
              size="sm"
              onClick={loadValidationTasks}
              disabled={isLoading}
            >
              <CheckCircle className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`} />
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Stats Cards */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
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
                  <Clock className="h-4 w-4 text-yellow-500" />
                  <span className="text-sm font-medium">Pending</span>
                </div>
                <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 text-blue-500" />
                  <span className="text-sm font-medium">In Progress</span>
                </div>
                <p className="text-2xl font-bold text-blue-600">{stats.in_progress}</p>
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
                  <XCircle className="h-4 w-4 text-red-500" />
                  <span className="text-sm font-medium">Rejected</span>
                </div>
                <p className="text-2xl font-bold text-red-600">{stats.rejected}</p>
              </CardContent>
            </Card>
          </div>

          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="all">All ({stats.total})</TabsTrigger>
              <TabsTrigger value="pending">Pending ({stats.pending})</TabsTrigger>
              <TabsTrigger value="in_progress">In Progress ({stats.in_progress})</TabsTrigger>
              <TabsTrigger value="completed">Completed ({stats.completed})</TabsTrigger>
              <TabsTrigger value="rejected">Rejected ({stats.rejected})</TabsTrigger>
            </TabsList>
          </Tabs>

          {/* Tasks Table */}
          <div className="border rounded-lg">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Document</TableHead>
                  <TableHead>Field</TableHead>
                  <TableHead>AI Confidence</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Assigned</TableHead>
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
                        <div className="h-4 bg-muted rounded w-20 animate-pulse" />
                      </TableCell>
                      <TableCell>
                        <div className="h-4 bg-muted rounded w-16 animate-pulse" />
                      </TableCell>
                      <TableCell>
                        <div className="h-6 bg-muted rounded w-20 animate-pulse" />
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
                            {task.document.document_type}
                          </p>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className="text-xs">
                          {task.field_name}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <span className="text-sm">{task.ai_confidence}%</span>
                          <div className="w-12 h-2 bg-muted rounded-full overflow-hidden">
                            <div 
                              className={`h-full ${
                                task.ai_confidence >= 80 ? "bg-green-500" :
                                task.ai_confidence >= 60 ? "bg-yellow-500" : "bg-red-500"
                              }`}
                              style={{ width: `${task.ai_confidence}%` }}
                            />
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(task.status)}
                          {getStatusBadge(task.status)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <p className="text-sm">{formatDate(task.assigned_at)}</p>
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
                        <CheckCircle className="mx-auto h-12 w-12 mb-4 opacity-50" />
                        <p>No validation tasks found</p>
                        <p className="text-sm">
                          {activeTab === "all" 
                            ? "No validation tasks available"
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
        </CardContent>
      </Card>

      {/* Validation Modal */}
      {selectedTask && (
        <ValidationModal
          task={selectedTask}
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedTask(null);
          }}
          onSubmit={handleSubmitValidation}
        />
      )}
    </div>
  );
}
