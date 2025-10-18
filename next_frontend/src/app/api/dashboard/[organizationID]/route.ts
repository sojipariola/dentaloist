// next_frontend/src/app/api/dashboard/[organizationID]/route.ts

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma'; // or your db client

export async function GET(
  request: Request,
  { params }: { params: { organizationId: string } }
) {
  const { organizationId } = params;

  try {
    // Example with Prisma
    const totalPatients = await prisma.patient.count({
      where: { organizationId },
    });

    const totalAppointments = await prisma.appointment.count({
      where: { organizationId },
    });

    const revenue = await prisma.invoice.aggregate({
      _sum: { amount: true },
      where: { organizationId },
    });

    const pendingTasks = await prisma.task.count({
      where: { organizationId, status: 'PENDING' },
    });

    return NextResponse.json({
      totalPatients,
      totalAppointments,
      revenue: revenue._sum.amount ?? 0,
      pendingTasks,
    });
  } catch (error) {
    console.error('Dashboard API error:', error);
    return NextResponse.json({ error: 'Failed to fetch dashboard data' }, { status: 500 });
  }
}
