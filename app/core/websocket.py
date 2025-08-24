"""
WebSocket Server Infrastructure for DocuMind™
Provides real-time communication foundation for Claude to implement
"""

import asyncio
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user_ws
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections with tenant isolation"""
    
    def __init__(self):
        # Tenant -> User -> Connection mapping
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        # Connection -> User mapping for cleanup
        self.connection_users: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, tenant_id: str):
        """Connect a user to WebSocket with tenant isolation"""
        await websocket.accept()
        
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = {}
        
        self.active_connections[tenant_id][user_id] = websocket
        self.connection_users[websocket] = {
            "user_id": user_id,
            "tenant_id": tenant_id
        }
        
        logger.info(f"User {user_id} connected to tenant {tenant_id}")
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a user from WebSocket"""
        if websocket in self.connection_users:
            user_info = self.connection_users[websocket]
            tenant_id = user_info["tenant_id"]
            user_id = user_info["user_id"]
            
            if tenant_id in self.active_connections:
                if user_id in self.active_connections[tenant_id]:
                    del self.active_connections[tenant_id][user_id]
                
                # Clean up empty tenant
                if not self.active_connections[tenant_id]:
                    del self.active_connections[tenant_id]
            
            del self.connection_users[websocket]
            logger.info(f"User {user_id} disconnected from tenant {tenant_id}")
    
    async def send_personal_message(self, message: str, user_id: str, tenant_id: str):
        """Send message to specific user in tenant"""
        if tenant_id in self.active_connections and user_id in self.active_connections[tenant_id]:
            websocket = self.active_connections[tenant_id][user_id]
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message to user {user_id}: {e}")
                self.disconnect(websocket)
    
    async def broadcast_to_tenant(self, message: str, tenant_id: str, exclude_user: Optional[str] = None):
        """Broadcast message to all users in a tenant"""
        if tenant_id in self.active_connections:
            disconnected_users = []
            for user_id, websocket in self.active_connections[tenant_id].items():
                if user_id != exclude_user:
                    try:
                        await websocket.send_text(message)
                    except Exception as e:
                        logger.error(f"Failed to broadcast to user {user_id}: {e}")
                        disconnected_users.append(user_id)
            
            # Clean up disconnected users
            for user_id in disconnected_users:
                if tenant_id in self.active_connections and user_id in self.active_connections[tenant_id]:
                    websocket = self.active_connections[tenant_id][user_id]
                    self.disconnect(websocket)

# Global connection manager
manager = ConnectionManager()

# WebSocket event types for Claude to implement
class WebSocketEvents:
    """WebSocket event types and handlers for Claude to implement"""
    
    # Document processing events
    DOCUMENT_UPLOAD_PROGRESS = "document.upload.progress"
    DOCUMENT_PROCESSING_UPDATE = "document.processing.update"
    DOCUMENT_PROCESSING_COMPLETE = "document.processing.complete"
    
    # Validation events
    VALIDATION_TASK_ASSIGNED = "validation.task.assigned"
    VALIDATION_TASK_UPDATED = "validation.task.updated"
    VALIDATION_TASK_COMPLETED = "validation.task.completed"
    
    # Chat events
    CHAT_MESSAGE_RECEIVED = "chat.message.received"
    CHAT_MESSAGE_STREAMING = "chat.message.streaming"
    CHAT_MESSAGE_COMPLETE = "chat.message.complete"
    
    # System events
    SYSTEM_NOTIFICATION = "system.notification"
    USER_STATUS_UPDATE = "user.status.update"

async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time communication
    Claude should implement the specific event handlers
    """
    try:
        # Authenticate user (Claude should implement proper auth)
        user = await get_current_user_ws(websocket, db)
        if not user:
            await websocket.close(code=4001, reason="Authentication failed")
            return
        
        # Connect user
        await manager.connect(websocket, str(user.id), str(user.tenant_id))
        
        # Send connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection.established",
            "data": {
                "user_id": str(user.id),
                "tenant_id": str(user.tenant_id)
            }
        }))
        
        # Main message loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Route message to appropriate handler
                await handle_websocket_message(message, user, db)
                
            except WebSocketDisconnect:
                manager.disconnect(websocket)
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "data": {"message": "Internal server error"}
                }))
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        await websocket.close(code=4000, reason="Connection error")

async def handle_websocket_message(message: Dict[str, Any], user: Any, db: Session):
    """
    Route WebSocket messages to appropriate handlers
    Claude should implement the specific event handlers
    """
    event_type = message.get("type")
    
    # TODO: Claude should implement these handlers
    if event_type == WebSocketEvents.DOCUMENT_UPLOAD_PROGRESS:
        # Handle document upload progress
        pass
    elif event_type == WebSocketEvents.VALIDATION_TASK_ASSIGNED:
        # Handle validation task assignment
        pass
    elif event_type == WebSocketEvents.CHAT_MESSAGE_RECEIVED:
        # Handle chat message
        pass
    else:
        logger.warning(f"Unknown WebSocket event type: {event_type}")

# Utility functions for Claude to use
async def broadcast_document_progress(
    tenant_id: str,
    document_id: str,
    progress: int,
    status: str,
    exclude_user: Optional[str] = None
):
    """Broadcast document processing progress to tenant"""
    message = json.dumps({
        "type": WebSocketEvents.DOCUMENT_PROCESSING_UPDATE,
        "data": {
            "document_id": document_id,
            "progress": progress,
            "status": status
        }
    })
    await manager.broadcast_to_tenant(message, tenant_id, exclude_user)

async def send_validation_notification(
    user_id: str,
    tenant_id: str,
    task_id: str,
    task_type: str
):
    """Send validation task notification to specific user"""
    message = json.dumps({
        "type": WebSocketEvents.VALIDATION_TASK_ASSIGNED,
        "data": {
            "task_id": task_id,
            "task_type": task_type
        }
    })
    await manager.send_personal_message(message, user_id, tenant_id)
